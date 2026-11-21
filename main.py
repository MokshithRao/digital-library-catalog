from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from routers.home import router as home_router



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



