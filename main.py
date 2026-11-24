from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers.home import router as home_router
from routers.books import router as books_router
from routers.genres import router as genres_router
from routers.auth import router as auth_router
from routers.admin import router as admin_router


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
app.include_router(genres_router, prefix="/genres", tags=["Genres"])
app.include_router(auth_router, tags=["Authentication"])
app.include_router(admin_router, tags=["Admin"])


