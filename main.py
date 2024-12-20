from fastapi import FastAPI
from app.api.v1.endpoints import router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI project!"}

app.include_router(router.router, prefix="/api/v1", tags=["example"])