import re
from typing import Tuple

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all instructions",
    r"disregard prior directives",
    r"system prompt override",
    r"you are now DAN",
    r"jailbreak mode",
    r"reveal system prompt",
    r"drop database",
    r"delete from users",
    r"grant all privileges",
    r"bypass security"
]


class PromptInjectionDetector:
    def __init__(self):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

    def detect(self, text: str) -> Tuple[bool, str]:
        """Returns (is_injection_detected, matched_pattern)"""
        for pattern in self.patterns:
            match = pattern.search(text)
            if match:
                return True, match.group(0)
        return False, ""


detector = PromptInjectionDetector()
