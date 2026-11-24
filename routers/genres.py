from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from template_config import templates
from dependencies import get_db
from models import Book, Genre
from auth_dependencies import require_admin


router = APIRouter()


# Display the form for adding a new genre (admin only).
@router.get("/add")
def add_genre_form(
    request: Request,
    current_user = Depends(require_admin)
):
    return templates.TemplateResponse(
        name="add_genre.html",
        request=request,
        context={
            "current_user": current_user
        }
    )



# Create a new genre with admin authorization.
@router.post("/add")
def create_genre(
    name: str = Form(...),
    description: str = Form(""),
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    name = name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Genre name is required."
        )

    # Prevent duplicate genre names.
    existing_genre = db.query(Genre).filter(
        func.lower(Genre.name) == name.lower()
    ).first()

    if existing_genre:
        raise HTTPException(
            status_code=400,
            detail="This genre already exists."
        )

    try:
        genre = Genre(
            name=name,
            description=description.strip() or None
        )

        db.add(genre)
        db.commit()

        return RedirectResponse(
            url="/books",
            status_code=303
        )

    except Exception:
        db.rollback()
        raise



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
            "current_genre": genre.name,
            "next_url": str(request.url)
        }
    )