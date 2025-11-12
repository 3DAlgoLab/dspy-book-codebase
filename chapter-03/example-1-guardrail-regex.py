import re

LEGAL_URL = "https://valueequity.com/legal/ai-disclaimer"

# Patterns for sensitive data
ACCOUNT_NUMBER_PATTERN = r'\b\d{10,16}\b'  # 10-16 digit account numbers
FOLIO_NUMBER_PATTERN = r'\b[A-Z]{2,4}\d{6,10}\b'  # Folio format: 2-4 letters + 6-10 digits

def check_disclaimer(content: str) -> bool:
    return LEGAL_URL in content if content else False

def contains_account_number(content: str) -> bool:
    """Check if content contains unmasked account numbers."""
    if not content:
        return False
    return bool(re.search(ACCOUNT_NUMBER_PATTERN, content))

def contains_folio_number(content: str) -> bool:
    """Check if content contains unmasked folio numbers."""
    if not content:
        return False
    return bool(re.search(FOLIO_NUMBER_PATTERN, content))

def is_content_safe(content: str) -> bool:
    """Check if content is safe (has disclaimer and no leaked sensitive data)."""
    if not content:
        return False
    
    has_disclaimer = check_disclaimer(content)
    has_leaked_account = contains_account_number(content)
    has_leaked_folio = contains_folio_number(content)
    
    return has_disclaimer and not has_leaked_account and not has_leaked_folio

if __name__ == "__main__":
    test_contents = [
        "This is a safe content. For more info, visit https://valueequity.com/legal/ai-disclaimer",
        "This content has an account number 12345678901234 but no disclaimer.",
        "This content has a folio number AB12345678 and the disclaimer https://valueequity.com/legal/ai-disclaimer",
        "This content is completely safe with the disclaimer https://valueequity.com/legal/ai-disclaimer and no sensitive data."
    ]
    
    for i, content in enumerate(test_contents):
        print(f"Content {i+1} is safe: {is_content_safe(content)}")