from fastapi import FastAPI
from models import Base, db

app = FastAPI()

from routes.auth_routes import auth_router
from routes.user_routes import user_router

app.include_router(auth_router)
app.include_router(user_router)