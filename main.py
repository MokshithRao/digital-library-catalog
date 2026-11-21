from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from routers.home import router as home_router
from routers.books import router as books_router



app = FastAPI(
    title="Digital Library Catalog",
    description="A web-based catalog for exploring books, authors, and genres.",
    version="1.0.0"
)



app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(home_router)
app.include_router(books_router, prefix="/books", tags=["Books"])


