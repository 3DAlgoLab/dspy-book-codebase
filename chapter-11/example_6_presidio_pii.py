from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

def scrub_pii_data():
    text_data = """
    CONFIDENTIAL BACKGROUND CHECK REPORT
    -----------------------------------
    Subject: Mr. Vikram Sharma
    Nationality: Indian
    Current Location: Bangalore, Karnataka
    Date of Report: 2023-10-25 at 14:30 PM

    CONTACT & DIGITAL FOOTPRINT:
    The subject can be reached at vikram.sharma88@example.com or via phone 
    at +91 98765 12345. During the audit, we tracked login activity from 
    IP Address 203.0.113.45 accessing the domain https://www.vikram-portfolio.in.

    FINANCIAL ASSETS (GLOBAL):
    We identified a primary savings account linked to IBAN GB29 XABC 1016 0000 0000 00.
    A recent transaction was made using a Mastercard: 5105 1051 0510 5100.
    The subject also holds a Bitcoin wallet with address 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2.

    GOVERNMENT IDENTIFICATION (INDIA SPECIFIC):
    To verify identity, the following documents were submitted:
    1. Permanent Account Number (PAN): ABCDE1234F
       (Verified with Income Tax Department)
    
    2. Aadhaar Card Number: 5485 5000 8000
       (UIDAI Verification Pending)
       
    3. Indian Passport Number: J1234567
       (Valid until 2030)
       
    4. Vehicle Registration: KA 05 AB 1234
       (Registered in Karnataka)
    """

    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    
    target_entities = [
        "PERSON",           # Names
        "LOCATION",         # Cities, Countries
        "EMAIL_ADDRESS",    # Email
        "PHONE_NUMBER",     # Phone numbers
        "IP_ADDRESS",       # IPv4/IPv6
        "URL",              # Websites
        "DATE_TIME",        # Dates
        "NRP",              # Nationality, Religious, Political groups
        "CREDIT_CARD",      # CCI
        "CRYPTO",           # Crypto Wallets
        "IBAN_CODE",        # International Bank Account Numbers        
        "IN_PAN",           # Permanent Account Number (10 chars alphanumeric)
        "IN_AADHAAR",       # 12-digit UIDAI number
        "IN_PASSPORT",      # Indian Passport
        "IN_VEHICLE_REGISTRATION" # Indian License Plates
    ]

    results = analyzer.analyze(
        text=text_data,
        language='en',
        entities=target_entities,
        score_threshold=0.4  # Set slightly lower to catch varied formats
    )

    print(f"Found {len(results)} entities. Anonymizing...")
    
    anonymized_result = anonymizer.anonymize(
        text=text_data,
        analyzer_results=results
    )

    return anonymized_result.text

if __name__ == "__main__":
    final_output = scrub_pii_data()
    print("\n" + "="*40)
    print("FINAL REDACTED OUTPUT")
    print("="*40)
    print(final_output)