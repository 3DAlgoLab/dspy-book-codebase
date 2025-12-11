import torch
from transformers import AutoTokenizer, AutoModel

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name) # <1>
model = AutoModel.from_pretrained(model_name) # <2>

text = "it doesn't matter if the cat is black or white as long as it catches mice"
print(f"Sentence: '{text}'\n")

inputs = tokenizer(text, return_tensors="pt") # <3>
input_ids = inputs["input_ids"][0]

tokens = tokenizer.convert_ids_to_tokens(input_ids) # <4>
print(f"1. Aligned Tokens: {tokens}")

outputs = model(**inputs) # <5>
embeddings = outputs.last_hidden_state

try:
    cat_index = tokens.index("cat")
    cat_vector = embeddings[0, cat_index] # <6>

    print(f"\n2. Found 'cat' at index: {cat_index}")
    print(f"3. Vector shape for 'cat': {cat_vector.shape}")
    print(f"4. First 10 numbers representing 'cat':\n{cat_vector[:10].tolist()}")

except ValueError:
    print("The word 'cat' was not found in the token list (it might have been split).")