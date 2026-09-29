from typing import Tuple, List, Dict, Any
from backend.app.security.prompt_injection import detector as injection_detector
from backend.app.security.pii_filter import pii_filter


class SecurityValidator:
    @staticmethod
    def validate_user_input(text: str) -> Tuple[bool, str, List[str]]:
        """
        Validates user query for prompt injection and PII.
        Returns: (is_safe, sanitized_text, safety_flags)
        """
        flags = []
        is_inj, pattern = injection_detector.detect(text)
        if is_inj:
            flags.append(f"PROMPT_INJECTION_DETECTED: {pattern}")
            return False, text, flags

        sanitized, pii_found = pii_filter.sanitize(text)
        if pii_found:
            flags.append(f"PII_REDACTED: {', '.join(pii_found)}")

        return True, sanitized, flags


validator = SecurityValidator()
