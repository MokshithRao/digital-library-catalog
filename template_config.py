import hashlib
from datetime import datetime

from fastapi.templating import Jinja2Templates

from database import SessionLocal
from models import User, UserSession


def get_template_context(request):
    # Identify the logged-in user for shared templates.
    current_user = None
    session_token = request.cookies.get("session_token")

    if session_token:
        token_hash = hashlib.sha256(session_token.encode()).hexdigest()

        db = SessionLocal()

        try:
            user_session = db.query(UserSession).filter(
                UserSession.token_hash == token_hash,
                UserSession.revoked_at.is_(None),
                UserSession.expires_at > datetime.utcnow()
            ).first()

            if user_session:
                current_user = db.query(User).filter(
                    User.id == user_session.user_id,
                    User.is_active == True
                ).first()

        finally:
            db.close()

    return {"current_user": current_user}


# Configure shared Jinja2 templates with authentication context.
templates = Jinja2Templates(
    directory="templates",
    context_processors=[get_template_context]
)