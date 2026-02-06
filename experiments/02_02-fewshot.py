import dspy

LOCAL_API_BASE = "http://127.0.0.1:8080/v1"

lm = dspy.LM(
    "openai/gpt-oss-20b",
    api_base=LOCAL_API_BASE,
    api_key="not-needed",
)

dspy.configure(lm=lm)


class MedicalCodingSignature(dspy.Signature):
    """Extract ICD-10 codes from clinical notes."""

    clinical_note = dspy.InputField(desc="Clinical documentation")
    icd10_codes = dspy.OutputField(desc="Comma-separated ICD-10 codes")
    rationale = dspy.OutputField(desc="Explanation for code selection")


demos = [
    dspy.Example(
        clinical_note="Patient presents with acute bronchitis, productive cough for 5 days",
        icd10_codes="J20.9",
        rationale="J20.9 is acute bronchitis, unspecified",
    ).with_inputs("clinical_note"),
    dspy.Example(
        clinical_note="Type 2 diabetes mellitus with diabetic neuropathy",
        icd10_codes="E11.40",
        rationale="E11.40 covers T2DM with neurological complications",
    ).with_inputs("clinical_note"),
]

# Use BootstrapFewShot to compile the few-shot model
few_shot_compiler = dspy.BootstrapFewShot(metric=lambda x, y: x == y)
medical_coder_with_demos = few_shot_compiler.compile(
    dspy.Predict(MedicalCodingSignature),
    trainset=demos,
)

# Test on new case
result = medical_coder_with_demos(
    clinical_note="Patient diagnosed with hypertensive heart disease with heart failure"
)
print(f"ICD-10 Codes: {result.icd10_codes}")
print(f"Rationale: {result.rationale}")
