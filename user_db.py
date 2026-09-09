from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase   

DATABASE_URL = "postgresql://postgres:Chetan%40090302@localhost:5432/Users"

engine = create_engine(DATABASE_URL,echo=True)
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
