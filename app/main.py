from fastapi import FastAPI

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
