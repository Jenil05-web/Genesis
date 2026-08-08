# Progress in 4 days :

Production code so far (src/):

config.py — a typed settings schema (pydantic-settings) that reads all env vars (API keys, storage paths) from .env into one settings object every other file imports from.

src/rag/chroma_client.py — opens a persistent connection to ChromaDB on disk and creates/returns the disaster_protocols collection. Pure connection setup, no data logic.

src/rag/build_knowledge_base.py — reads real PDFs (FEMA + 3 NDMA manuals) from data/raw/protocols/, splits each into clean sentence-boundary chunks, tags each chunk by disaster type (guessed from filename), and saves ~1911 chunks into ChromaDB as searchable vectors.

src/rag/search_knowledge_base.py — takes a plain question + optional disaster type, searches the saved chunks semantically, and returns the most relevant real text — filtered to that disaster type plus general guidance.

