from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Modelo de Guardias
class Guard(Base):
    __tablename__ = "guardias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    comuna = Column(String, nullable=False)

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///./guardias.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)