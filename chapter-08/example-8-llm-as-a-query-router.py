import dspy
from typing import Literal
from pydantic import BaseModel, Field

QueryType = Literal["FACT_LOOKUP", "REASONING", "HYBRID"]

class DecomposedQuery(BaseModel):
    """A single decomposed sub-query with its routing type."""
    query: str = Field(description="Self-contained sub-query")
    type: QueryType = Field(description="The routing type for this sub-query")

class QueryRouter(dspy.Signature):
    """Analyze a user query and decompose or break it down into sub-queries such that each sub-query focuses on one thing only.

    - FACT_LOOKUP: Point queries seeking discrete, atomic information (specific metrics, identifiers, timestamps, or well-defined entities)
    - REASONING: Analytical tasks requiring synthesis across information (pattern identification, causal analysis, multi-document summarization, or comparative evaluation)
    - HYBRID: Complex queries combining broad information discovery with deep analytical processing (corpus-wide trend analysis, filtered aggregations, or multi-step reasoning over search results)
    
    If the query has a single intent, return one sub-query.
    If the query has multiple intents, decompose into independent sub-queries.
    Each sub-query should be self-contained so ensure it has the required context and understandable without the original.
    """
    
    query: str = dspy.InputField(desc="The user's original query")
    sub_queries: list[DecomposedQuery] = dspy.OutputField(
        desc="List of decomposed sub-queries with their routing types"
    )

def print_result(query, result):
    """Print the router result in a formatted way."""
    print(f"\nOriginal Query: {query}")
    print(f"Number of sub-queries: {len(result.sub_queries)}\n")
    for i, sub_query in enumerate(result.sub_queries, 1):
        print(f"  [{i}] Type: {sub_query.type}")
        print(f"      Query: {sub_query.query}\n")

if __name__ == "__main__":
    dspy.configure(lm=dspy.LM('gemini/gemini-2.5-flash'))    
    router = dspy.Predict(QueryRouter)
    
    query = (
        "What is the current Federal Funds Rate, "
        "how does the current yield curve inversion severity compare to the 2008 financial crisis, "
        "and based on the last 20 years of S&P 500 data, which sectors historically outperform "
        "during the 6 months following a rate cut?"
    )
    
    result = router(query=query)
    print_result(query, result)