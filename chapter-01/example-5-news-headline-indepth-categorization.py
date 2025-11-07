import dspy
from typing import Literal, List


class NewsArticleCategorization(dspy.Signature):
    """Analyze and categorize news articles with comprehensive information
    extraction."""

    article: str = dspy.InputField(desc="The complete news article text to be analyzed")
    category: Literal[
        "Politics",
        "Business",
        "Sports",
        "Technology",
        "Health",
        "Entertainment",
        "World News",
        "Science",
        "Crime",
        "Weather",
    ] = dspy.OutputField(desc="The most appropriate news category for the article")
    entities: List[str] = dspy.OutputField(
        desc="Key people, organizations, locations, and other named entities mentioned in the article"
    )
    facts: List[str] = dspy.OutputField(
        desc="Important factual statements and key information from the article"
    )
    sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField(
        desc="Overall emotional tone and sentiment of the article"
    )
    topics: List[str] = dspy.OutputField(
        desc="Main themes and subject matters discussed in the article"
    )
    summary: str = dspy.OutputField(
        desc="Concise summary capturing the essential points of the article"
    )
