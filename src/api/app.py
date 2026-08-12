import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import incidents, health
from src.db.session import create_db_and_tables
from src.utils.helpers import configure_logging

configure_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("genesis")


def create_app() -> FastAPI:
    app = FastAPI(title="Genesis Disaster Response API")
    create_db_and_tables()
    logger.info("Genesis API starting — env=%s", os.getenv("ENVIRONMENT", "dev"))

    # Always allow the deployed Render frontend. Also picks up any FRONTEND_URL env var
    # so local dev (wildcard) and staging URLs work without code changes.
    allowed_origins = {"https://genesis-frontend-xfzy.onrender.com"}
    frontend_url = os.getenv("FRONTEND_URL", "")
    if frontend_url:
        allowed_origins.add(frontend_url)
    # Fall back to wildcard only if no specific origins are set (local dev safety net)
    origins = list(allowed_origins) if allowed_origins else ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(incidents.router)
    return app


app = create_app()