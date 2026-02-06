import dspy
from dspy.predict.program_of_thought import PythonInterpreter  # <1>

lm = dspy.LM("lm_studio/qwen/qwen3-coder-next")
dspy.configure(lm=lm)


investment_calculator = dspy.ProgramOfThought(
    "initial_investment, monthly_contribution, annual_return, years -> generated_code",
    interpreter=PythonInterpreter(),
    max_iters=5,
)

result = investment_calculator(
    initial_investment="$10,000",
    monthly_contribution="$500",
    annual_return="7.5%",
    years="20",
)

print(f"Generated Code:\n{result.generated_code}\n")
