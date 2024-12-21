from fastapi import APIRouter, Depends, HTTPException
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
@router.post("/create_guard")
def add_guardia(guardia: GuardiaCreate, db: Session = Depends(get_db)):
    print("Datos recibidos:", guardia)
    try:
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
    except Exception as e:
        print("Error al guardar el guardia:", e)
        raise HTTPException(status_code=500, detail="Error al guardar el guardia")

@router.delete("/guardias/{guardia_id}")
def delete_guardia(guardia_id: int, db: Session = Depends(get_db)):
    guardia = db.query(Guardia).get(guardia_id)
     # Verificar si el guardia existe
    if not guardia:
        raise HTTPException(status_code=404, detail="Guardia no encontrado")
    db.delete(guardia)
    db.commit()
    return {"message": "Guardia eliminado"}

@router.get("/guardias/")
def get_guardias(db: Session = Depends(get_db)):
    return db.query(Guardia).all()