import dspy
from dspy.evaluate import Evaluate

lm = dspy.LM('gemini/gemini-2.0-flash') 
dspy.configure(lm=lm)

support_data = [ # <1>
    dspy.Example( 
        question="How do I compose a new email in Gmail?",
        answer="Click the 'Compose' button in the top-left corner"
    ).with_inputs("question"),  # <2>
    dspy.Example(
        question="How can I search for an old email?",
        answer="Use the search bar at the top of your Gmail inbox"
    ).with_inputs("question"),
    dspy.Example(
        question="How do I add a signature to my emails?",
        answer="Go to Settings > See all settings > General > Signature"
    ).with_inputs("question"),
    dspy.Example(
        question="What's the easiest way to delete an email?",
        answer="Open the email and click the trash can icon"
    ).with_inputs("question"),
]

def support_quality_metric(example, pred, trace=None):  # <3>
    """
    Checks if the answer contains key information from the correct answer
    """
    gold_answer = example.answer.lower().replace('.', '').replace(',', '')
    pred_answer = pred.answer.lower().replace('.', '').replace(',', '')
    gold_keywords = set(gold_answer.split()) 
    pred_keywords = set(pred_answer.split())

    overlap = len(gold_keywords & pred_keywords)  # <4>
    total = len(gold_keywords)

    if total == 0:
        return False

    return (overlap / total) >= 0.5  # <5>

class SupportBot(dspy.Signature):
    """Answer customer support questions accurately and helpfully"""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="Clear, accurate answer")

chatbot = dspy.ChainOfThought(SupportBot)
evaluator = Evaluate(  # <6>
    devset=support_data,
    metric=support_quality_metric,
    num_threads=2,
    display_progress=True
)

score = evaluator(chatbot)  # <7>
print(f"Chatbot Accuracy: {score.score:.1f}%")
