import dspy

MODEL_CONFIGS = [  # <1>
    ("gemini/gemini-2.5-pro", "primary"),
    ("gemini/gemini-2.5-flash", "secondary"),
    ("openai/gpt-3.5-turbo", "tertiary"),
]

class QA(dspy.Signature):
    question = dspy.InputField()
    answer = dspy.OutputField()

def try_model(model_name: str, prompt: str, tier: str) -> dict:
    lm = dspy.LM(model=model_name)
    with dspy.context(lm=lm):  # <2>
        predictor = dspy.Predict(QA)
        response = predictor(question=prompt)
    return {
        "response": response.answer,
        "model": model_name,
        "tier": tier
    }

def get_completion_with_fallback(prompt: str, model_configs: list) -> dict:
    for model_name, tier in model_configs:  # <3>
        try:
            return try_model(model_name, prompt, tier)
        except Exception as e:
            print(f"{tier.capitalize()} model ({model_name}) failed: {e}")  # <4>
            continue  # <5>
    
    return {  # <6>
        "response": "I'm experiencing technical difficulties. Please try again later.",
        "model": "static",
        "tier": "fallback"
    }

result = get_completion_with_fallback("Explain quantum computing", MODEL_CONFIGS)
print(f"Response from {result['model']} ({result['tier']}): {result['response']}")

