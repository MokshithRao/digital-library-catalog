from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dependencies import get_db
from models import Book, Genre

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def list_books(
    request: Request, 
    search: str = None,
    genre_id: str = "",
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))

    if genre_id:
        query = query.filter(Book.genre_id == int(genre_id))

    books = query.all()
    genres = db.query(Genre).all()

    return templates.TemplateResponse(
        name="listing.html",
        request=request,
        context={
            "books": books,
            "search": search,
            "genres": genres,
            "selected_genre": genre_id
        }
    )



@router.get("/{book_id}")
def book_details(
    book_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return templates.TemplateResponse(
        name="details.html",
        request=request,
        context={"book": book}
    )


