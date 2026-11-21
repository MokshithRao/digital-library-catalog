from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dependencies import get_db
from models import Book, Genre


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/{genre_id}")
def genre_books(
    genre_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()

    if not genre:
        raise HTTPException(
            status_code=404,
            detail="Genre not found"
        )

    books = db.query(Book).filter(Book.genre_id == genre_id).all()
    genres = db.query(Genre).all()

    return templates.TemplateResponse(
        name="listing.html",
        request=request,
        context={
            "books": books,
            "genres": genres,
            "search": "",
            "selected_genre": genre_id,
            "current_genre": genre.name
        }
    )