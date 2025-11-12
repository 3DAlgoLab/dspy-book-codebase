# Chapter 3

## Prerequisites

Make sure you have a running environment with all packages installed.

- If not, refer to the [Project README for instructions](../README.md).

## Example Scripts in Chapter 3

This chapter focuses on guardrails and evaluation techniques for DSPy applications, demonstrating how to ensure safe and compliant AI outputs:

- [example-1-guardrail-regex.py](example-1-guardrail-regex.py): Regex-based guardrails for detecting sensitive data (account numbers, folio numbers) and checking for legal disclaimers.
- [example-2-guardrail-llm-as-judge.py](example-2-guardrail-llm-as-judge.py): Using LLM as a judge to evaluate investment compliance, detecting unlicensed advice and guaranteed return promises.
- [example-3-support-bot.py](example-3-support-bot.py): Building and evaluating a customer support chatbot with custom quality metrics and DSPy's Evaluate framework.

## How to Run

To run any example, activate your environment and execute the desired script. For example:

```bash
# macOS / Linux
source ../env/bin/activate
python example-1-guardrail-regex.py

# Windows (PowerShell)
../env/Scripts/Activate.ps1
python example-1-guardrail-regex.py

# Windows (cmd.exe)
..\env\Scripts\activate.bat
python example-1-guardrail-regex.py
```
> Tip: On many macOS / Linux systems you may use `python3` and `pip3`. On Windows, `python` and `pip` are typically the correct commands.

## Example Output

```bash
(env) ank@Ankurs-MacBook-Air chapter-03 % python example-1-guardrail-regex.py
```

```shell
(env12) ank@Ankurs-MacBook-Air code % python example-1-guardrail-regex.py
Content 1 is safe: True
Content 2 is safe: False
Content 3 is safe: False
Content 4 is safe: True
```

```bash
(env12) ank@Ankurs-MacBook-Air code % python example-2-guardrail-llm-as-judge.py
Investment Advice: True
Guaranteed Returns: False
Reasoning: The content states "Stick to current stocks." This is a recommendation to hold specific assets, which constitutes investment advice. There is no mention of guaranteed returns.

Investment Advice: False
Guaranteed Returns: False
Reasoning: The content states that a portfolio has grown by 12% based on market performance. This is a statement of past performance and does not contain any advice to buy or sell, nor does it guarantee any future returns.
```

```bash
(env12) ank@Ankurs-MacBook-Air code % python example-3-support-bot.py
Average Metric: 3.00 / 4 (75.0%): 100%|█████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 38.17it/s]
2025/11/12 20:13:23 INFO dspy.evaluate.evaluate: Average Metric: 3 / 4 (75.0%)
Chatbot Accuracy: 75.0%
```
