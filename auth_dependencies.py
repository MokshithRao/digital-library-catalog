import hashlib
from datetime import datetime

from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from models import User, UserSession


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    # Read the session token from the browser cookie.
    session_token = request.cookies.get("session_token")

    if not session_token:
        raise HTTPException(status_code=401, detail="Please log in.")

    # Hash the token to find its database session.
    token_hash = hashlib.sha256(session_token.encode()).hexdigest()

    user_session = db.query(UserSession).filter(
        UserSession.token_hash == token_hash,
        UserSession.revoked_at.is_(None),
        UserSession.expires_at > datetime.utcnow()
    ).first()

    if not user_session:
        raise HTTPException(status_code=401, detail="Session expired or invalid.")

    # Retrieve the active user associated with the session.
    user = db.query(User).filter(
        User.id == user_session.user_id,
        User.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User account is inactive.")

    return user


def require_admin(
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required."
        )
    return current_user