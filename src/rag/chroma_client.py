#  This file only sets up the connection: the persistent client (disk location) and the collection (a named bucket inside Chroma, wired to know it should use OpenAI's embedding model).

import chromadb

from chromadb.utils import embedding_functions

from src.config import settings

_client = None
_collection = None

def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    return _client



def get_protocol_collection():
    global _collection
    if _collection is None:
        client = get_chroma_client()
        embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name="text-embedding-3-small",
        )
        _collection = client.get_or_create_collection(
            name="disaster_protocols",
            embedding_function=embedding_fn,
        )
    return _collection


# This file by itself doesn't do embedding or search — it 
#  Think of it as "opening the database and picking which table to use," not "storing/searching data."