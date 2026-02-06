import dspy 
from icecream import ic 

LOCAL_API_BASE = "http://127.0.0.1:8080/v1"

lm = dspy.LM(
    "openai/gpt-oss-20b",
    api_base=LOCAL_API_BASE,
    api_key="not-needed",
)

dspy.configure(lm=lm)

class QA(dspy.Signature):
    """Answer questions with step-by-step reasoning"""
    question = dspy.InputField()
    answer = dspy.OutputField()
    
cot_predict = dspy.ChainOfThought(QA)
question = "If a train travels 120 miles in 2 hours, what is its speed?"

cot_result= cot_predict(question=question)

ic(cot_result.answer)
ic(cot_result.reasoning)