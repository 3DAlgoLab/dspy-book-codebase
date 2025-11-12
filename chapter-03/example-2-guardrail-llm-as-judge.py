import dspy
lm = dspy.LM('gemini/gemini-2.0-flash')
dspy.configure(lm=lm)

class InvestmentComplianceSignature(dspy.Signature):
    """Evaluate if content contains unlicensed investment advice or guaranteed return promises."""
    
    content: str = dspy.InputField(desc="The response content to evaluate")
    reasoning: str = dspy.OutputField(desc="Step-by-step reasoning about compliance issues")
    contains_investment_advice: bool = dspy.OutputField(desc="Boolean: True if content contains unlicensed investment advice like 'buy', 'sell', or specific recommendations") 
    contains_guaranteed_returns: bool = dspy.OutputField(desc="Boolean: True if content promises or guarantees specific returns or profits") # <1>

class InvestmentComplianceJudge(dspy.Module):
    def __init__(self):
        super().__init__()
        self.judge = dspy.ChainOfThought(InvestmentComplianceSignature) # <2>
    
    def forward(self, content):
        result = self.judge(content=content)
        return result

judge = InvestmentComplianceJudge()

# Example 1: Contains investment advice (FAIL)
response = judge(content="Your portfolio has grown 12% this year. Stick to current stocks.")
print(f"Investment Advice: {response.contains_investment_advice}")
print(f"Guaranteed Returns: {response.contains_guaranteed_returns}")
print(f"Reasoning: {response.reasoning}")

# Example 2: Informational only (PASS)
response2 = judge(content="Your portfolio has grown 12% this year based on market performance.")
print(f"\nInvestment Advice: {response2.contains_investment_advice}")
print(f"Guaranteed Returns: {response2.contains_guaranteed_returns}")
print(f"Reasoning: {response2.reasoning}")
