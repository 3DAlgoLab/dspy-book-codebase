import dspy
from common import set_lm_model

set_lm_model()


class ClassifyNews(dspy.Signature):
    news_article = dspy.InputField(desc="The full text of the news article.")
    news_category = dspy.OutputField(
        desc="A single category, e.g., 'Politics', 'Sports', 'Technology', 'Other."
    )
    
class NewsClassifier(dspy.Module):
    def __init__(self):
        super().__init__()
        self.classifier = dspy.Predict(ClassifyNews)
        
    def forward(self, news_article):
        return self.classifier(news_article=news_article)
    
    
classifier = NewsClassifier()
result = classifier(news_article="India reduces GST rates.")
print(result.news_category)