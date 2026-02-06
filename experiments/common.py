import dspy


def set_lm_model(model_id="qwen/qwen3-coder-30b", max_tokens=15_000, temperature=0.3):
    lm = dspy.LM(
        model=f"lm_studio/{model_id}", max_tokens=max_tokens, temperature=temperature
    )
    dspy.configure(lm=lm)
    return lm

