from pydantic import BaseModel

class GuardiaCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    comuna: str