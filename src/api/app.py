from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import incidents, health
from src.db.session import create_db_and_tables

def create_app() -> FastAPI:
    app = FastAPI(title="Genesis Disaster Response API")
    create_db_and_tables()

    # Allow requests from the HTML frontend (served locally or via file://)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(incidents.router)
    return app

app = create_app()