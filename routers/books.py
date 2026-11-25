from fastapi import APIRouter, Request, Depends, HTTPException, Form, File, UploadFile
from fastapi.responses import RedirectResponse
from pathlib import Path
from uuid import uuid4
from sqlalchemy import func
from sqlalchemy.orm import Session
from template_config import templates
from dependencies import get_db
from models import Book, Genre, Author
from auth_dependencies import require_admin

router = APIRouter()


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



# Display the form for adding a new book (admin only).
@router.get("/add")
def add_book_form(
    request: Request,
    current_user= Depends(require_admin),
    db: Session = Depends(get_db)
):
    authors = db.query(Author).order_by(Author.name.asc()).all()
    genres = db.query(Genre).order_by(Genre.name.asc()).all()

    return templates.TemplateResponse(
        name="add_book.html",
        request=request,
        context={
            "authors": authors,
            "genres": genres,
            "current_user": current_user
        }
    )



# Create a new book and its author (if needed), with admin authorization.
@router.post("/add")
async def create_book(
    title: str = Form(...),
    description: str = Form(""),
    isbn: str = Form(""),
    publisher: str = Form(""),
    publication_year: str = Form(""),
    genre_id: int = Form(...),
    author_mode: str = Form(...),
    author_id: str = Form(""),
    author_name: str = Form(""),
    author_biography: str = Form(""),
    is_available: str = Form("true"),
    cover_image: UploadFile = File(...),
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    image_path = None

    try:
        # Validate the uploaded image.
        allowed_types = {"image/jpeg", "image/png", "image/webp"}

        if cover_image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG and WebP images are allowed."
            )

        extension = Path(cover_image.filename).suffix.lower()

        if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
            raise HTTPException(
                status_code=400,
                detail="Invalid image extension."
            )

        image_directory = Path("static/images")
        image_directory.mkdir(parents=True, exist_ok=True)

        image_filename = f"{uuid4().hex}{extension}"
        image_path = image_directory / image_filename

        image_data = await cover_image.read()

        if not image_data:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty."
            )

        if len(image_data) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="Image size must not exceed 5 MB."
            )

        image_path.write_bytes(image_data)

        # Validate the publication year.
        publication_year_value = None

        if publication_year.strip():
            try:
                publication_year_value = int(publication_year)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Publication year must be a valid number."
                )

        # Validate author selection.
        if author_mode not in {"existing", "new"}:
            raise HTTPException(
                status_code=400,
                detail="Invalid author selection."
            )

        # Validate availability selection.
        if is_available not in {"true", "false"}:
            raise HTTPException(
                status_code=400,
                detail="Invalid availability value."
            )

        # Check whether the selected genre exists.
        genre = db.query(Genre).filter(
            Genre.id == genre_id
        ).first()

        if not genre:
            raise HTTPException(
                status_code=400,
                detail="Selected genre does not exist."
            )

        # Select an existing author or create a new one.
        if author_mode == "existing":

            if not author_id.isdigit():
                raise HTTPException(
                    status_code=400,
                    detail="Please select an author."
                )

            author = db.query(Author).filter(
                Author.id == int(author_id)
            ).first()

            if not author:
                raise HTTPException(
                    status_code=400,
                    detail="Selected author does not exist."
                )

        else:
            if not author_name.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Author name is required."
                )

            author = db.query(Author).filter(
                func.lower(Author.name) == author_name.strip().lower()
            ).first()

            if not author:
                author = Author(
                    name=author_name.strip(),
                    biography=author_biography.strip() or None
                )

                db.add(author)
                db.flush()

        # Create the new book.
        book = Book(
            title=title.strip(),
            description=description.strip() or None,
            isbn=isbn.strip() or None,
            publisher=publisher.strip() or None,
            publication_year=publication_year_value,
            cover_image=image_filename,
            is_available=(is_available == "true"),
            author_id=author.id,
            genre_id=genre.id
        )

        db.add(book)

        # Commit author and book together.
        db.commit()

        return RedirectResponse(
            url="/books",
            status_code=303
        )

    except Exception:
        # Roll back database changes if anything fails.
        db.rollback()

        # Remove uploaded image if database processing fails.
        if image_path and image_path.exists():
            image_path.unlink()

        raise

    finally:
        await cover_image.close()




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



# Display the edit form for an existing book (admin only).
@router.get("/{book_id}/edit")
def edit_book_form(
    book_id: int,
    request: Request,
    current_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found."
        )

    authors = db.query(Author).order_by(Author.name.asc()).all()
    genres = db.query(Genre).order_by(Genre.name.asc()).all()

    return templates.TemplateResponse(
        name="edit_book.html",
        request=request,
        context={
            "book": book,
            "authors": authors,
            "genres": genres,
            "current_user": current_user
        }
    )





# Update an existing book with admin authorization.
@router.post("/{book_id}/edit")
async def update_book(
    book_id: int,
    title: str = Form(...),
    description: str = Form(""),
    isbn: str = Form(""),
    publisher: str = Form(""),
    publication_year: str = Form(""),
    genre_id: int = Form(...),
    author_id: int = Form(...),
    is_available: str = Form("true"),
    cover_image: UploadFile = File(None),
    current_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    image_path = None

    try:
        book = db.query(Book).filter(Book.id == book_id).first()

        if not book:
            raise HTTPException(
                status_code=404,
                detail="Book not found."
            )

        genre = db.query(Genre).filter(
            Genre.id == genre_id
        ).first()

        author = db.query(Author).filter(
            Author.id == author_id
        ).first()

        if not genre or not author:
            raise HTTPException(
                status_code=400,
                detail="Invalid author or genre selection."
            )

        if is_available not in {"true", "false"}:
            raise HTTPException(
                status_code=400,
                detail="Invalid availability value."
            )

        publication_year_value = None

        if publication_year.strip():
            try:
                publication_year_value = int(publication_year)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Publication year must be a valid number."
                )

        new_image_filename = None

        # Process a new cover image if one was uploaded.
        if cover_image and cover_image.filename:

            allowed_types = {"image/jpeg", "image/png", "image/webp"}

            if cover_image.content_type not in allowed_types:
                raise HTTPException(
                    status_code=400,
                    detail="Only JPEG, PNG and WebP images are allowed."
                )

            extension = Path(cover_image.filename).suffix.lower()

            if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid image extension."
                )

            image_data = await cover_image.read()

            if not image_data:
                raise HTTPException(
                    status_code=400,
                    detail="Uploaded image is empty."
                )

            if len(image_data) > 5 * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail="Image size must not exceed 5 MB."
                )

            image_directory = Path("static/images")
            image_directory.mkdir(parents=True, exist_ok=True)

            new_image_filename = f"{uuid4().hex}{extension}"
            image_path = image_directory / new_image_filename

            image_path.write_bytes(image_data)

        # Update book details.
        book.title = title.strip()
        book.description = description.strip() or None
        book.isbn = isbn.strip() or None
        book.publisher = publisher.strip() or None
        book.publication_year = publication_year_value
        book.genre_id = genre.id
        book.author_id = author.id
        book.is_available = (is_available == "true")

        if new_image_filename:
            book.cover_image = new_image_filename

        db.commit()

        return RedirectResponse(
            url=f"/books/{book.id}",
            status_code=303
        )

    except Exception:
        db.rollback()

        if image_path and image_path.exists():
            image_path.unlink()

        raise

    finally:
        if cover_image:
            await cover_image.close()




# Delete an existing book with admin authorization.
@router.post("/{book_id}/delete")
def delete_book(
    book_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail= "Book not found."
        )

    try:
        image_filename = book.cover_image

        db.delete(book)
        db.commit()

        if image_filename:
            image_directory = Path("static/images").resolve()
            image_path = (image_directory / image_filename).resolve()

            if image_path.parent == image_directory and image_path.is_file():
                image_path.unlink()

        return RedirectResponse(
            url='/books',
            status_code=303
        )

    except Exception:
        db.rollback()
        raise