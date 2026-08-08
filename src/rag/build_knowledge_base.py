 # This file turns our 4 PDFs into ChromaDB's stored knowledge.
# 4 PDFs → broken into small overlapping paragraphs → each paragraph tagged by disaster type → each paragraph converted to a searchable vector → saved.


"""This file handles the "Data Ingestion" part of a RAG (Retrieval-Augmented Generation) system.
 It takes raw files (like PDFs), breaks them down, and stores them in ChromaDB (a vector database) 
 so that they can be easily searched later to answer questions."""


from pathlib import Path # this is used to 
from pypdf import PdfReader
import re

from src.rag.chroma_client import get_protocol_collection

PROTOCOLS_FOLDER = Path("data/raw/protocols")
CHUNK_SIZE = 800
OVERLAP = 100
DISASTER_TYPES = ["flood", "earthquake", "fire", "storm", "hurricane", "cyclone"]


def read_file(path: Path) -> str:
    """Reads a PDF, markdown, or text file and returns its full text as one string."""
    if path.suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if path.suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    raise ValueError(f"Can't read this file type: {path.suffix}")


def split_into_chunks(text: str, size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """Splits text into chunks on sentence boundaries, so words never get cut mid-way."""
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) <= size:
            current += " " + sentence
        else:
            if current.strip():
                chunks.append(current.strip())
            current = sentence
    if current.strip():
        chunks.append(current.strip())

    return chunks


def guess_disaster_type(filename: str) -> str:
    """Reads the disaster type straight from the filename, e.g. 'flood_fema.pdf' -> 'flood'."""
    lower = filename.lower()
    for dtype in DISASTER_TYPES:
        if dtype in lower:
            return dtype
    return "general"


def build_knowledge_base(folder: Path = PROTOCOLS_FOLDER) -> int:
    """Reads every file in the folder, chunks it, tags it, and saves it into ChromaDB."""
    collection = get_protocol_collection()
    total = 0

    for file_path in folder.glob("*"):
        if file_path.suffix not in {".pdf", ".md", ".txt"}:
            continue

        full_text = read_file(file_path)
        chunks = split_into_chunks(full_text)
        disaster_type = guess_disaster_type(file_path.name)

        collection.add(
            ids=[f"{file_path.stem}_{i}" for i in range(len(chunks))],
            documents=chunks,
            metadatas=[{"source": file_path.name, "disaster_type": disaster_type} for _ in chunks],
        )
        print(f"Saved {len(chunks)} chunks from {file_path.name} (tagged: {disaster_type})")
        total += len(chunks)

    return total


if __name__ == "__main__":
    total = build_knowledge_base()
    print(f"Total chunks saved: {total}")