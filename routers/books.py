from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dependencies import get_db
from models import Book

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def list_books(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()

    return templates.TemplateResponse(
        name="listing.html",
        request=request,
        context={"books": books}
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
