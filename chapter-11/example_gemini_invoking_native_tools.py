import dspy

tools = [{"googleSearch": {}}]
dspy.configure(lm=dspy.LM("gemini/gemini-3-pro-preview"))

pred = dspy.Predict("question -> answer")
print(pred(question="What is your knowledge cut-off date?."))

pred = dspy.Predict("question -> answer", tools=tools)
print(pred(question="Give only the name of the Current Mayor of New York?."))