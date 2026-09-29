import re
from typing import Tuple, List

# Regexes for common PII: SSN, Credit Cards, Emails, Phone numbers
SSN_REGEX = r"\b\d{3}-\d{2}-\d{4}\b"
CREDIT_CARD_REGEX = r"\b(?:\d[ -]*?){13,16}\b"
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
PHONE_REGEX = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"


class PIIFilter:
    def sanitize(self, text: str) -> Tuple[str, List[str]]:
        found_pii = []
        sanitized = text

        if re.search(SSN_REGEX, sanitized):
            found_pii.append("SSN")
            sanitized = re.sub(SSN_REGEX, "[REDACTED_SSN]", sanitized)

        if re.search(CREDIT_CARD_REGEX, sanitized):
            # Exclude standard 16 digit IDs if they are not actual credit cards by checking length
            matches = re.findall(CREDIT_CARD_REGEX, sanitized)
            for m in matches:
                digits_only = re.sub(r"\D", "", m)
                if len(digits_only) in [15, 16] and not m.startswith("PRD_"):
                    found_pii.append("CREDIT_CARD")
                    sanitized = sanitized.replace(m, "[REDACTED_CARD]")

        return sanitized, list(set(found_pii))


pii_filter = PIIFilter()
