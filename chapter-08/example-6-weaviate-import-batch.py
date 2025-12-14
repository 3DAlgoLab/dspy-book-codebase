import weaviate
from weaviate.util import generate_uuid5
import pandas as pd
import os

client = weaviate.connect_to_local()

df = pd.read_csv("financial_qa.csv")

financial_qa = client.collections.get("FinancialQA")

with financial_qa.batch.fixed_size(batch_size=100) as batch:
    for i, row in df.iterrows():
        qa_obj = {
            "question": row["question"],
            "answer": row["answer"],
            "context": row["context"],
            "ticker": row["ticker"],
            "filing": row["filing"],
        }
        batch.add_object(
            properties=qa_obj,
            uuid=generate_uuid5(f"{row['ticker']}_{row['question']}")
        )

total_count = financial_qa.aggregate.over_all(total_count=True)
print(f"Total documents in FinancialQA collection: {total_count.total_count}")

client.close()
