from datasets import load_dataset

_dataset = None
def load_sample_messages(n: int = 5)-> list[dict]:
    """Loads n messages from the disaster-tweets dataset (dev/eval replay source).
    Returns the same normalized shape as fetch_news, so Alert Monitor doesn't
    care which source it came from."""

    global _dataset
    if _dataset is None :
        _dataset = load_dataset("venetis/disaster_tweets")["train"]


    rows = _dataset.select(range(n))
    return [
        {
            "text": row["text"],
            "source": "dataset_replay",
            "location_hint": row.get("location"),
            "timestamp": None,
        }
        for row in rows
    ]

    

 
