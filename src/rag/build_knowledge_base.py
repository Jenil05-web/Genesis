from pathlib import Path
from pypdf import PdfReader

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
    """Cuts one long string into small overlapping pieces, so each piece is searchable on its own."""
    chunks, start = [], 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end].strip())
        start = end - overlap
    return [c for c in chunks if c]


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