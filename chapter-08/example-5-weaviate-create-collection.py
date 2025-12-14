import weaviate
from weaviate.classes.config import Configure, Property, DataType
import os

client = weaviate.connect_to_local()

client.collections.create(
    name="FinancialQA",
    properties=[
        Property(name="question", data_type=DataType.TEXT),
        Property(name="answer", data_type=DataType.TEXT),
        Property(name="context", data_type=DataType.TEXT),
        Property(name="ticker", data_type=DataType.TEXT),
        Property(name="filing", data_type=DataType.TEXT),
    ],
    vectorizer_config=Configure.Vectorizer.text2vec_model2vec(),
)

client.close()
