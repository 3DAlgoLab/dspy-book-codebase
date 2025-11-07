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
    """Categorize news headlines into appropriate news categories."""
    headline: str = dspy.InputField(desc="The news headline text to be categorized")
    category: NewsCategory = dspy.OutputField(desc="The most appropriate news category for the given headline")