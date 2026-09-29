import hashlib
import os

SECRET_SALT = "finai_nexus_salt_2026"


def get_password_hash(password: str) -> str:
    """Generates SHA-256 salted hash for user passwords."""
    salted = f"{SECRET_SALT}:{password}"
    return hashlib.sha256(salted.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password against hashed password."""
    return get_password_hash(plain_password) == hashed_password
