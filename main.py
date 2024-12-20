from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"] 
)

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI project!"}

app.include_router(router.router, prefix="/api/v1", tags=["example"])
