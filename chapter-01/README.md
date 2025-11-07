
# Chapter 1

## Prerequisites

Make sure you have a running environment with all packages installed.

- If not, refer to the [Project README for instructions](../README.md).

## Ollama Setup

Install Ollama: Download from [Ollama Download Page](https://ollama.com/download)

```bash
ollama pull phi3:mini
```

## Example Scripts in Chapter 1

This chapter contains several example scripts demonstrating basic DSPy and LLM usage:

- [example-1-hello-ai.py](example-1-hello-ai.py): Basic hello world with an AI model.
- [example-2-setup-dspy.py](example-2-setup-dspy.py): Shows how to set up DSPy in your environment.
- [example-3-feedback-analysis.py](example-3-feedback-analysis.py): Analyzes feedback using LLMs.
- [example-4-news-headline-category.py](example-4-news-headline-category.py): Categorizes news headlines using LLMs.
- [example-4-news-headline-indepth-categorization.py](example-4-news-headline-indepth-categorization.py): Provides in-depth categorization of news headlines.
- [example-5-news-headline-indepth-categorization.py](example-5-news-headline-indepth-categorization.py): Further in-depth categorization example.
- [example-6-new-product-analysis.py](example-6-new-product-analysis.py): Analyzes new product ideas using LLMs.
- [utils.py](utils.py): Utility functions used by the examples.

## How to Run

To run any example, activate your environment and execute the desired script. For example:

```bash
source ../env/bin/activate
python example-1-hello-ai.py
```

## Example Output

Let us execute the hello world script and see the response from the phi3:mini model:

```bash
python example-1-hello-ai.py
['Hello, world! How can I help you today?']
```