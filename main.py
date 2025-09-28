from fastapi import FastAPI
from models import Base, db

app = FastAPI()
Base.metadata.create_all(bind=db)

from routes.auth_routes import auth_router

app.include_router(auth_router)