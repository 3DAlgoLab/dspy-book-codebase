import json
import os
import re

import dspy
import pandas as pd
import weaviate
import weaviate.classes.config as wvc
from weaviate.classes.query import HybridFusion, MetadataQuery

CONFIG = {
    "collection_name": "financial_qa",  # <1>
    "csv_path": "financial_qa.csv",  # <2>
    "rerank_model_name": "ollama_chat/Qwen3-Reranker-4B",  # <3>
    "ollama_url": "http://localhost:11434",  # <4>
    "main_model_name": "gemini/gemini-2.5-flash",  # <5>
    "gemini_api_key": os.getenv("GEMINI_API_KEY"),  # <6>
    "top_k": 100,  # <7>
    "retrieve_limit": 30,  # <8>
    "alpha": 0.5,  # <9>
    "rerank_batch_size": 5  # <10>
}

class FinancialRelevance(dspy.Signature):
    """
    Analyze the numbered passages and select the ones that BEST answer the specific query.
    
    RELEVANCE CRITERIA (Prioritize these):
    1. EXPLICIT FACTS: Passages containing exact numbers (e.g., "$1.35 billion"), dates ("1999"), or specific product names ("H100", "RTX 40").
    2. DEFINITIONS: Passages that define a strategy or term (e.g., "Platform strategy is...") over those that just mention it.
    3. PENALIZE: Downgrade vague marketing fluff or general forward-looking statements without substance.
    """
    query = dspy.InputField(desc="The financial question")
    passages = dspy.InputField(desc="Numbered list of candidate texts")
    
    audit_reasoning = dspy.OutputField(desc="Why these specific passages beat the others, Brief check of which passages contain the hard facts")
    best_indices = dspy.OutputField(desc="A JSON list of integers for the most relevant passages (e.g., [0, 3])")


class FinancialAnswerSignature(dspy.Signature):
    """
    Answer the financial question using ONLY the provided context.
    Cite the context if possible. If the answer is not in the context, state that.
    """
    context = dspy.InputField(desc="Relevant text explaining the theme of the question and the answer")
    question = dspy.InputField(desc="The user's question")
    answer = dspy.OutputField(desc="Detailed answer based on the context")


class ListwiseReranker(dspy.Module):
    def __init__(self, local_lm):
        super().__init__()
        self.lm = local_lm
        self.prog = dspy.ChainOfThought(FinancialRelevance)

    def _deduplicate(self, raw_passages):
        return list(dict.fromkeys(raw_passages))

    def _format_batch(self, batch):
        # Format: "[0] Text... \n [1] Text..."
        return "\n\n".join([f"[{idx}] {p[:500]}..." for idx, p in enumerate(batch)])

    def _extract_indices(self, best_indices_output, batch_len):
        # Capture the content inside brackets (e.g., "0, 1, 3")
        # Regex explanation: Match '[' then capture digits/commas/spaces then ']'
        matches = re.findall(r'\[([\d,\s]+)\]', str(best_indices_output))
        
        selected_indices = []
        for match in matches:
            # Split the captured string "0, 1, 3" by comma
            parts = match.split(',')
            for part in parts:
                try:
                    # Strip whitespace and convert to int
                    idx = int(part.strip())
                    # Validate index is within batch bounds
                    if 0 <= idx < batch_len:
                        selected_indices.append(idx)
                except ValueError:
                    continue
                    
        return list(set(selected_indices))  # Deduplicate results

    def _process_batch(self, query, batch, batch_index):
        passages_str = self._format_batch(batch)
        try:
            pred = self.prog(query=query, passages=passages_str)
            valid_indices = self._extract_indices(pred.best_indices, len(batch))
            
            # Map batch indices back to actual text
            return [batch[idx] for idx in valid_indices]
                            
        except Exception as e:
            print(f"  [Reranker Error] Batch {batch_index} skipped: {e}")
            return []

    def _run_reranking_loop(self, query, unique_passages):
        winners = []
        print(f"  > Reranking {len(unique_passages)} unique passages...")

        with dspy.context(lm=self.lm):
            for i in range(0, len(unique_passages), CONFIG["rerank_batch_size"]):
                batch = unique_passages[i : i + CONFIG["rerank_batch_size"]]
                batch_winners = self._process_batch(query, batch, i)
                winners.extend(batch_winners)
        return winners

    def _backfill(self, winners, unique_passages):
        # Fallback: If strict criteria yielded too few results, fill from vector search top results
        final_selection = []
        seen = set()
        
        # Add winners first
        for p in winners:
            if p not in seen:
                final_selection.append(p)
                seen.add(p)
        
        # Backfill if needed
        if len(final_selection) < CONFIG["top_k"]:
            for p in unique_passages:
                if p not in seen:
                    final_selection.append(p)
                    seen.add(p)
                    if len(final_selection) >= CONFIG["top_k"]:
                        break
                        
        return final_selection[:CONFIG["top_k"]]

    def forward(self, query, raw_passages):
        """
        Reranks passages by auditing them in batches against the Financial Relevance criteria.
        """
        unique_passages = self._deduplicate(raw_passages)
        winners = self._run_reranking_loop(query, unique_passages)
        return self._backfill(winners, unique_passages)

class HybridRetriever(dspy.Retrieve):
    def __init__(self, client, local_lm):
        super().__init__()
        self.client = client
        self.collection = client.collections.get(CONFIG["collection_name"])
        self.reranker = ListwiseReranker(local_lm)

    def forward(self, query_or_queries, k=None) -> dspy.Prediction:
        query = query_or_queries[0] if isinstance(query_or_queries, list) else query_or_queries
        
        response = self.collection.query.hybrid(
            query=query,
            alpha=CONFIG["alpha"],
            limit=CONFIG["retrieve_limit"],
            fusion_type=HybridFusion.RELATIVE_SCORE
        )
        
        raw_passages = [obj.properties.get("context", "") for obj in response.objects]
        
        if not raw_passages:
            return dspy.Prediction(passages=[])

        selected_passages = self.reranker(query=query, raw_passages=raw_passages)
        
        return dspy.Prediction(passages=selected_passages)


class FinancialRAG(dspy.Module):
    def __init__(self, retriever):
        super().__init__()
        self.retriever = retriever
        self.prog = dspy.ChainOfThought(FinancialAnswerSignature)

    def forward(self, question):
        results = self.retriever(question)        
        context = "\n\n".join([f"[Source {i+1}]: {p}" for i, p in enumerate(results.passages)])

        return self.prog(context=context, question=question)


def setup_weaviate(client):
    if client.collections.exists(CONFIG["collection_name"]):
        return

    print(f"Creating collection '{CONFIG['collection_name']}'...")
    client.collections.create(
        name=CONFIG["collection_name"],
        vectorizer_config=wvc.Configure.Vectorizer.text2vec_model2vec(),
        properties=[
            wvc.Property(name="context", data_type=wvc.DataType.TEXT),
            wvc.Property(name="ticker", data_type=wvc.DataType.TEXT),
            wvc.Property(name="filing", data_type=wvc.DataType.TEXT),
        ]
    )

    if os.path.exists(CONFIG["csv_path"]):
        df = pd.read_csv(CONFIG["csv_path"])
        print(f"Indexing {len(df)} rows...")
        collection = client.collections.get(CONFIG["collection_name"])
        with collection.batch.dynamic() as batch:
            for _, row in df.iterrows():
                batch.add_object(properties={
                    "context": str(row.get("context", "")),
                    "ticker": str(row.get("ticker", "N/A")),
                    "filing": str(row.get("filing", "N/A"))
                })
        print("Indexing complete.")

def main():
    try:
        client = weaviate.connect_to_local()
        client.collections.delete(CONFIG["collection_name"])
        setup_weaviate(client)
    except Exception as e:
        print(f"Weaviate Error: {e}")
        return

    local_lm = dspy.LM(
        model=CONFIG["rerank_model_name"], 
        api_base=CONFIG["ollama_url"], 
        api_key=""
    )

    gemini_lm = dspy.LM(
        model=CONFIG["main_model_name"], 
        api_key=CONFIG["gemini_api_key"]
    )
    
    dspy.configure(lm=gemini_lm)

    retriever = HybridRetriever(client, local_lm)
    rag = FinancialRAG(retriever)

    while True:
        q = input("\nQuestion (or 'exit'): ")
        if q.lower() in ["exit", "quit"]: break
        
        print("*" * 40)
        try:
            pred = rag(q)
            print(f"ANSWER:\n{pred.answer}\n")
            print(f"REASONING:\n{pred.reasoning}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 40)

    client.close()

if __name__ == "__main__":
    main()
