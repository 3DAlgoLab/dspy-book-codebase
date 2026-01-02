import dspy
import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import MetadataQuery
from datetime import datetime, timedelta

gemini = dspy.LM(model="gemini/gemini-2.5-pro")
dspy.configure(lm=gemini)  # <1>

client = weaviate.connect_to_local()  # <2>

if not client.collections.exists("SemanticCache"):  # <3>
    client.collections.create(
        name="SemanticCache",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # <4>
        properties=[
            wvc.config.Property(name="query", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="answer", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="timestamp", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="feedback_score", data_type=wvc.config.DataType.INT),  # <5>
            wvc.config.Property(name="usage_count", data_type=wvc.config.DataType.INT),
        ]
    )

class QA(dspy.Signature):
    """Answer questions"""
    question = dspy.InputField()
    answer = dspy.OutputField()

def semantic_cache_lookup(
    query: str,
    threshold: float = 0.95,  # <1>
    max_age_hours: int = 24
) -> dict | None:

    collection = client.collections.get("SemanticCache")

    response = collection.query.near_text(  # <2>
        query=query,
        limit=1,
        return_metadata=MetadataQuery(distance=True)
    )

    if not response.objects:
        return None

    result = response.objects[0]
    similarity = 1 - result.metadata.distance  # <3>

    cached_time = datetime.fromisoformat(result.properties['timestamp'])
    age = datetime.now() - cached_time

    if similarity >= threshold and age < timedelta(hours=max_age_hours):  # <4>
        print(f"Semantic cache hit! Similarity: {similarity:.3f}")
        return {
            'answer': result.properties['answer'],
            'similarity': similarity,
            'cache_id': result.uuid,
            'from_cache': True
        }

    return None

def store_in_cache(query: str, answer: str) -> str:
    collection = client.collections.get("SemanticCache")

    cache_id = collection.data.insert({
        'query': query,
        'answer': answer,
        'timestamp': datetime.now().isoformat(),
        'feedback_score': 0,
        'usage_count': 0
    })

    return cache_id

def record_feedback(cache_id: str, thumbs_up: bool):  # <5>
    collection = client.collections.get("SemanticCache")
    cached_item = collection.query.fetch_object_by_id(cache_id)

    current_score = cached_item.properties.get('feedback_score', 0)
    new_score = current_score + (1 if thumbs_up else -1)

    collection.data.update(
        uuid=cache_id,
        properties={'feedback_score': new_score}
    )

    if new_score < -3:  # <6>
        print(f"Cache entry {cache_id} invalidated due to negative feedback")
        collection.data.delete_by_id(cache_id)

def get_llm_response_cached(query: str) -> dict:  # <1>
    
    cached_result = semantic_cache_lookup(query, threshold=0.95)
    if cached_result:  # <2>
        collection = client.collections.get("SemanticCache")
        collection.data.update(
            uuid=cached_result['cache_id'],
            properties={'usage_count': 
                collection.query.fetch_object_by_id(
                    cached_result['cache_id']
                ).properties['usage_count'] + 1
            }
        )
        return cached_result
    
    print("Calling LLM (no semantic match found)")
    predictor = dspy.Predict(QA)
    response = predictor(question=query)  # <3>
    answer = response.answer
    
    cache_id = store_in_cache(query, answer)  # <4>
    
    return {
        'answer': answer,
        'similarity': 1.0,
        'cache_id': cache_id,
        'from_cache': False
    }

if __name__ == "__main__":
    result = get_llm_response_cached("How do I reset my password?")
    print(f"Answer: {result['answer']}")
    print(f"From cache: {result['from_cache']}")

    user_satisfied = True
    record_feedback(result['cache_id'], thumbs_up=user_satisfied)  # <5>

    result2 = get_llm_response_cached("What are the password reset steps?")  # <6>
    print(f"Cache hit: {result2['from_cache']}")

