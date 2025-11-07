import dspy

lm = dspy.LM("ollama_chat/phi3:mini", max_tokens=4000)
dspy.configure(lm=lm)

response = lm("Hello World!")
print(response)