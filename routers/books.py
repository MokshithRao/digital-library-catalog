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
    sort_by: str = "title",
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))

    if genre_id:
        query = query.filter(Book.genre_id == int(genre_id))

# Apply the selected sorting order to the books query.
    if sort_by == "title":
        query = query.order_by(Book.title.asc())

    elif sort_by == "title_desc":
        query = query.order_by(Book.title.desc())

    elif sort_by == "year_asc":
        query = query.order_by(Book.publication_year.asc())

    elif sort_by == "year_desc":
        query = query.order_by(Book.publication_year.desc())

    else:
        query = query.order_by(Book.title.asc())



    books = query.all()
    genres = db.query(Genre).all()

    return templates.TemplateResponse(
        name="listing.html",
        request=request,
        context={
            "books": books,
            "search": search,
            "genres": genres,
            "selected_genre": genre_id,
            "sort_by": sort_by,
            "next_url": request.url.path + (
    "?" + request.url.query if request.url.query else "")

        }
    )



@router.get("/{book_id}")
def book_details(
    book_id: int,
    request: Request,
    next_url: str = "/books",
    db: Session = Depends(get_db)
):

    if not next_url.startswith("/") or next_url.startswith("//"):
        next_url = "/books"

    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return templates.TemplateResponse(
        name="details.html",
        request=request,
        context={
            "book": book,
            "next_url": next_url
        }
    )


