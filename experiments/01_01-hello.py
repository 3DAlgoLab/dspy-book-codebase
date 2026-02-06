import dspy 

lm = dspy.LM("lm_studio/mistralai/ministral-3-3b", max_tokens=20_000)
dspy.configure(lm=lm)

# response = lm("Hello Ai?")
# print(response)

response = lm("Where is Empire State Building?")
print(response)

