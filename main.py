from fastapi import FastAPI
from app.api.v1.endpoints import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Agrega el origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)
@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI project!"}

app.include_router(router.router, prefix="/api/v1", tags=["example"])