from sqlmodel import SQLModel , Session , create_engine
from src.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)

def create_db_and_tables():
    """Creates the SQLite file and all tables, if they don't already exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Yields a database session — use in a `with` block so it closes automatically."""
    with Session(engine) as session:
        yield session    


        """create_engine reads settings.DATABASE_URL (already sqlite:///./data/genesis.db in .env) — one connection setup, reused everywhere.
          create_db_and_tables() is a one-time setup call, 
        similar to build_knowledge_base.py's role for Chroma — run once before first use."""