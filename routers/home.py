from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated

from dependencies import get_db
from models import Genre, Book, User
from auth_dependencies import get_current_user


router = APIRouter()


templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):

    genres = db.query(Genre).all()
    featured_books = db.query(Book).limit(4).all()

    return templates.TemplateResponse(
        name="home.html",
        request=request,
        context={
            "genres": genres,
            "featured_books": featured_books
        }
    )


@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse(
        name="about.html",
        request=request
    )