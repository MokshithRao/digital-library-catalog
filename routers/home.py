from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from models import Genre, Book
from template_config import templates


router = APIRouter()



@router.get("/")
def home(
    request: Request,
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