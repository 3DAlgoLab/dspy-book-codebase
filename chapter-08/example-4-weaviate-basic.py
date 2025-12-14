import weaviate # <1>
from weaviate.classes.config import Configure, DataType, Property # <2>

# Financial news documents
documents = [
    "AlphaTech released a new AI processor for data centers",
    "BioCure announces successful trials for diabetes drug",
    "GlobalBank reports strong investment banking revenue",
    "AutoDrive reveals fully autonomous electric vehicle",
    "CloudNet suffers minor data breach but secures customer data"
]

companies = ["AlphaTech", "BioCure", "GlobalBank", "AutoDrive", "CloudNet"]

client = weaviate.connect_to_local() # <3>

if client.collections.exists("FinancialNews"): # <4>
    client.collections.delete("FinancialNews")

client.collections.create( # <5>
    name="FinancialNews",
    properties=[
        Property(name="content", data_type=DataType.TEXT),
        Property(name="company", data_type=DataType.TEXT)
    ], # <6>
    vector_config=Configure.Vectors.text2vec_model2vec(), # <7>
)

financial_news = client.collections.get("FinancialNews") # <8>
financial_news.data.insert_many([
    {"content": doc, "company": company}
    for doc, company in zip(documents, companies)
]) # <9>

# Perform semantic search
query = "artificial intelligence cpu"
results = financial_news.query.near_text(query=query, limit=1) # <10>

print(f"Query: {query}")
print(f"Best Match: {results.objects[0].properties['company']}")
print(f"Content: {results.objects[0].properties['content']}")

client.close() # <11>
