from fastapi import FastAPI
from backend.app.router import router


app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "API is working!"}
