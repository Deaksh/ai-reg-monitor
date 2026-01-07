import hashlib

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def chunk_paragraphs(paragraphs):
    chunks = []
    for idx, text in enumerate(paragraphs):
        chunks.append({
            "chunk_id": f"art32_p{idx}",
            "text": text,
            "hash": hash_text(text)
        })
    return chunks
