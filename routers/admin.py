from fastapi import APIRouter, Request, Depends
from typing import Annotated
from auth_dependencies import require_admin
from models import User, Book, Genre
from template_config import templates
from dependencies import get_db
from template_config import templates
from sqlalchemy.orm import Session


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