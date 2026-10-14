from fastapi import FastAPI


app = FastAPI(
    title="FastAPI Port",
    debug=True,
)

@app.get("/")
def root():
    return {
        "message": "Hello world"
    }
