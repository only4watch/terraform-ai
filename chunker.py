import re

def chunk_terraform_code(tf_text: str, chunk_size: int = 1000):
    chunks = []
    for i in range(0, len(tf_text), chunk_size):
        chunks.append(tf_text[i:i + chunk_size])
    return chunks
