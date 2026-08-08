"""IN this file we are basically """

from src.rag.chroma_client import get_protocol_collection

def search_protocols(question:str , disaster_type:str = None, top_results:int = 5)->list[str]:

    """Searches the knowledge base for protocols related to a given question and disaster type."""

    collection = get_protocol_collection()


    where_filter = None
    if disaster_type:
        where_filter = {"disaster_type": {"$in": [disaster_type, "general"]}}

    results = collection.query(
        query_texts = [question],
        n_results = top_results,
        where = where_filter,
    )
    return results["documents"][0]

