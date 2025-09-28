from models import db
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=db)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()