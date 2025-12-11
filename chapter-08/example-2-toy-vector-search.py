from sklearn.feature_extraction.text import TfidfVectorizer # <1>
from sklearn.metrics.pairwise import cosine_similarity # <2>
import numpy as np # <3>

documents = [
    "AlphaTech released a new AI processor for data centers", 
    "BioCure announces successful trials for diabetes drug",
    "GlobalBank reports strong investment banking revenue",
    "AutoDrive reveals fully autonomous electric vehicle",
    "CloudNet suffers minor data breach but secures customer data"
] 
companies = ["AlphaTech", "BioCure", "GlobalBank", "AutoDrive", "CloudNet"] # <4>

vectorizer = TfidfVectorizer() # <5>
tfidf_matrix = vectorizer.fit_transform(documents) # <6>

query_vector = vectorizer.transform(["AI processor"]) # <7>
similarities = cosine_similarity(query_vector, tfidf_matrix).flatten() # <8>

best_match = np.argmax(similarities) # <9>
print(f"Query: AI processor") # <10>
print(f"Best Match: {companies[best_match]}") # <11>
print(f"Similarity: {similarities[best_match]:.4f}") # <12>

