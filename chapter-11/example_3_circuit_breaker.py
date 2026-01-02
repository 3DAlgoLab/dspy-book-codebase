import dspy
from circuitbreaker import circuit, CircuitBreakerError  # <1>

# Configure DSPy with Gemini
gemini = dspy.LM(model="gemini/gemini-2.5-pro")
dspy.configure(lm=gemini)

class QA(dspy.Signature):
    """Answer questions"""
    question = dspy.InputField()
    answer = dspy.OutputField()

@circuit(failure_threshold=5, recovery_timeout=60)  # <2>
def call_gemini(prompt: str) -> str:
    """Call Gemini with circuit breaker protection"""
    predictor = dspy.Predict(QA)
    response = predictor(question=prompt)
    return response.answer

# Usage with fallback handling
def safe_call_gemini(prompt: str) -> str:
    try:
        return call_gemini(prompt)  # <3>
    except CircuitBreakerError as e:  # <4>
        print(f"Circuit breaker open: {e}")
        return "Service temporarily unavailable. Please try again later."
    except Exception as e:
        print(f"LLM call failed: {e}")
        return "An error occurred. Please try again."

# Example
result = safe_call_gemini("What is machine learning?")
print(result)
