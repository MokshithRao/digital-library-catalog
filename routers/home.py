from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dependencies import get_db
from models import Genre


router = APIRouter()


templates = Jinja2Templates(directory="templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    genres = db.query(Genre).all()

    return templates.TemplateResponse(
        name="home.html",
        request=request,
        context={"genres": genres}
    )


@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse(
        name="about.html",
        request=request
    )