import weaviate # <1>
from weaviate.classes.query import MetadataQuery, Filter, Rerank # <2>
import os

client = weaviate.connect_to_local() # <3>

financial_qa = client.collections.get("FinancialQA") # <4>

print("*** BM25 Keyword Search ***")
bm25_response = financial_qa.query.bm25( # <5>
    query="GPU deep learning",
    limit=3,
    query_properties=["question", "answer^2"], # <6>
    return_metadata=MetadataQuery(score=True) # <7>
)

for obj in bm25_response.objects:
    print(f"Question: {obj.properties['question'][:80]}...")
    print(f"BM25 Score: {obj.metadata.score:.3f}\n") # <8>

print("*** Vector Search ***")
vector_response = financial_qa.query.near_text( # <9>
    query="artificial intelligence hardware for servers",
    limit=3,
    return_metadata=MetadataQuery(distance=True) # <10>
)

for obj in vector_response.objects:
    print(f"Question: {obj.properties['question'][:80]}...")
    print(f"Answer: {obj.properties['answer'][:100]}...")
    print(f"Distance: {obj.metadata.distance:.3f}\n") # <11>

print("*** Hybrid Search ***")
hybrid_response = financial_qa.query.hybrid( # <12>
    query="platform strategy",
    alpha=0.5, # <13>
    limit=3,
    return_metadata=MetadataQuery(score=True)
)

for obj in hybrid_response.objects:
    print(f"Question: {obj.properties['question'][:80]}...")
    print(f"Filing: {obj.properties['filing']}")
    print(f"Hybrid Score: {obj.metadata.score:.3f}\n")

print("*** Vector Search with Filter ***")
filtered_response = financial_qa.query.near_text( # <14>
    query="company strategy and market position",
    limit=3,
    return_metadata=MetadataQuery(distance=True),
    filters=Filter.by_property("ticker").equal("NVDA") # <15>
)

for obj in filtered_response.objects:
    print(f"Question: {obj.properties['question'][:80]}...")
    print(f"Ticker: {obj.properties['ticker']}")
    print(f"Distance: {obj.metadata.distance:.3f}\n")

client.close() # <18>
