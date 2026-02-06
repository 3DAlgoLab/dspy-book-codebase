import dspy 
from typing import Literal 

NewsCategory = Literal[
    'Politics',
    'Business',
    'Sports',
    'Technology',
    'Health',
    'Entertainment',
    'World News',
    'Science',
    'Crime',
    'Weather'
]


class NewsHeadlineCategorization(dspy.Signature):
    """Categorize news headlines into appropriate news categories"""
    headline: str = dspy.InputField(desc="The news headline text to be categorized")
    category: NewsCategory = dspy.OutputField(desc="The most appropriate news category for the given headline")


lm = dspy.LM("lm_studio/qwen/qwen3-coder-30b", max_tokens=50_000)
dspy.configure(lm=lm)

categorizer = dspy.Predict(NewsHeadlineCategorization)    

headline = "New advancements in AI technology are transforming industries worldwide"

# get the prediction
result = categorizer(headline=headline)
print(result)