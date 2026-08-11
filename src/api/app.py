from fastapi import FastAPI

from src.api.routes import incidents, health
from src.db.session import create_db_and_tables

def create_app()-> FastAPI:
    app = FastAPI(title="Genesis Disaster Response API")
    create_db_and_tables()
    app.include_router(health.router)
    app.include_router(incidents.router)
    return app

app = create_app()