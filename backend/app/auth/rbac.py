from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.auth.jwt import decode_access_token
from backend.app.models.domain import User
from backend.app.core.exceptions import AuthenticationException, AuthorizationException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise AuthenticationException("Could not validate credentials")
    except Exception:
        raise AuthenticationException("Invalid authentication credentials")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise AuthenticationException("User not found or inactive")
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if user.role not in self.allowed_roles:
            raise AuthorizationException(f"Role '{user.role}' is not authorized. Allowed: {self.allowed_roles}")
        return user


require_admin = RoleChecker(["ADMIN"])
require_analyst = RoleChecker(["ADMIN", "ANALYST"])
require_viewer = RoleChecker(["ADMIN", "ANALYST", "VIEWER"])
