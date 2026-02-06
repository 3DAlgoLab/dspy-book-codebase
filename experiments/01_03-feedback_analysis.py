import json

import dspy


class FeedbackAnalysisSignature(dspy.Signature):
    """Analyze customer feedback and extract key themes categorized as positive or negative"""

    feedback = dspy.InputField(desc="Customer feedback to analyze")
    analysis = dspy.OutputField(
        desc="Use structure like: {'themes': {'negative': [], 'positive': []}} with key themes from feedback. Output ONLY valid JSON with no markdown fences (like ```json), prefixes, or extra text. "
    )


if __name__ == "__main__":
    lm = dspy.LM("lm_studio/openai/gpt-oss-20b", max_tokens=20000, temperature=0.3)
    dspy.configure(lm=lm)

    customer_feedback = """"The app crashes frequently on iOS, especially when uploading photos. The interface is confusing and I can't find the settings menu. However, I love the new dark mode feature and the photo filters are amazing so please fix the issues so I don't have to try other apps."""

    feedback_analyzer = dspy.ChainOfThought(FeedbackAnalysisSignature)
    result = feedback_analyzer(feedback=customer_feedback)

    if not result.analysis:
        print("Prediction Error!")
        import sys

        sys.exit(1)

    try:
        analysis_json = json.loads(result.analysis)
        print(analysis_json)
        print("\nParsed Analysis:")
        print(json.dumps(analysis_json, indent=2))
    except json.JSONDecodeError:
        print("NOTE: Response may not be valid JSON format.")
        print(result.analysis)
        if hasattr(result, "reasoning"):
            print(result.reasoning)

        dspy.inspect_history(10)

    input("\nFinish to Enter!")
