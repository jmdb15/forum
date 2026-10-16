from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.users.router import user_router

app = FastAPI(
    title="FastAPI Port",
    debug=True,
)

app.include_router(user_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "Hello world"
    }

app.mount(
    "/media",
    StaticFiles(directory="media", check_dir=False),
    name="media",
)
