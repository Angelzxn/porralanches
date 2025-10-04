from models import db
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=db)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def normalizar_texto(texto: str) -> str:
    if not texto.isalnum():
        return ''.join(e for e in texto if e.isalnum())
    return texto
