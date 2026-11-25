from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from typing import Annotated
from auth_dependencies import require_admin
from models import User, Book, Genre, UserSession
from template_config import templates
from dependencies import get_db
from template_config import templates
from sqlalchemy.orm import Session
from datetime import datetime


router = APIRouter(prefix="/admin")


@router.get("/", name="Admin_dashboard")
def admin_dashboard(
    request: Request,
    current_user: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)]
):
    total_books = db.query(Book).count()
    total_genres = db.query(Genre).count()
    total_users = db.query(User).count()

    total_admins = db.query(User).filter(User.role == 'admin').count()

    return templates.TemplateResponse(
        name="admin/dashboard.html",
        request=request,
        context={
            "current_user": current_user,
            "total_books": total_books,
            "total_genres": total_genres,
            "total_users": total_users,
            "total_admins": total_admins
            }
    )



# Display all registered users for admin management.
@router.get("/users")
def manage_users(
    request: Request,
    curret_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    users = db.query(User).order_by(User.created_at.desc()).all()

    return templates.TemplateResponse(
        name="admin/users.html",
        request=request,
        context={
            "users": users,
            "current_user": curret_user
        }
    )



# Activate or deactivate a user account (admin only).
@router.post("/users/{user_id}/toggle-status")
def toggle_user_status(
    user_id: int,
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot deactivate your own account."
        )

    user.is_active = not user.is_active

    # Revoke all active sessions when the account is deactivated.
    if not user.is_active:
        active_sessions = db.query(UserSession).filter(
            UserSession.user_id == user.id,
            UserSession.revoked_at.is_(None)
        ).all()

        for session in active_sessions:
            session.revoked_at = datetime.utcnow()


    db.commit()

    return RedirectResponse(
        url="/admin/users",
        status_code=303
    )