from fastapi import APIRouter, Depends
from app.repository.database import Guardia, SessionLocal
from sqlalchemy.orm import Session
from app.schemas.GuardSchema import GuardiaCreate
from app.core.gurobi import asignar_turnos

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/example")
async def read_example():
    return {"message": "This is an example endpoint."}


@router.post("/assign_shifts/")
def assign_shifts(db: Session = Depends(get_db)):
    guardias = db.query(Guardia).all()
    horarios = ["08:00-16:00", "16:00-00:00", "00:00-08:00"]  # Horarios de ejemplo

    nombres_guardias = [f"{g.nombre} {g.apellido}" for g in guardias]
    asignaciones = asignar_turnos(nombres_guardias, horarios)

    return {"asignaciones": asignaciones}

# Endpoint para agregar un guardia
@router.post("/guardias/")
def add_guardia(guardia: GuardiaCreate, db: Session = Depends(get_db)):
    new_guardia = Guardia(
        nombre=guardia.nombre,
        apellido=guardia.apellido,
        email=guardia.email,
        comuna=guardia.comuna,
    )
    db.add(new_guardia)
    db.commit()
    db.refresh(new_guardia)
    return new_guardia

@router.get("/guardias/")
def get_guardias(db: Session = Depends(get_db)):
    return db.query(Guardia).all()