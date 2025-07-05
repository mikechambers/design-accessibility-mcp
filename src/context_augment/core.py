import os
import numpy as np
import pickle
from openai import OpenAI

CHUNK_TOKEN_SIZE = 200
EMBEDDING_MODEL = "text-embedding-3-small"
MIN_SIMILARITY = 0.60

client = OpenAI()

def chunk_text(text, max_tokens=CHUNK_TOKEN_SIZE):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield " ".join(words[i:i + max_tokens])

def embed_documents(docs, batch_size=100):
    all_chunks = []
    chunks_to_embed = []
    chunk_metadata = []
    
    # Collect all chunks first
    for doc in docs:
        for chunk in chunk_text(doc["text"]):
            if chunk.strip():  # Skip empty chunks
                chunks_to_embed.append(chunk)
                chunk_metadata.append({"id": doc["id"], "text": chunk})

    print(f"Found {len(chunks_to_embed)} chunks to embed...")

    # Process in batches
    for i in range(0, len(chunks_to_embed), batch_size):
        batch = chunks_to_embed[i:i + batch_size]
        batch_metadata = chunk_metadata[i:i + batch_size]
        
        try:
            print(f"Embedding batch {i//batch_size + 1}/{(len(chunks_to_embed) + batch_size - 1)//batch_size}...")
            
            embedding_response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=batch
            )
            
            for j, embedding_data in enumerate(embedding_response.data):
                metadata = batch_metadata[j]
                all_chunks.append({
                    "id": metadata["id"],
                    "text": metadata["text"],
                    "embedding": embedding_data.embedding
                })
                
        except Exception as e:
            print(f"Error embedding batch {i//batch_size + 1}: {e}")
            print("Continuing with next batch...")
            continue

    print(f"Successfully embedded {len(all_chunks)} chunks")
    return all_chunks

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def retrieve_relevant_chunks(all_chunks, query, k=5):

    if not all_chunks:
        return []

    query_embedding = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    ).data[0].embedding

    scored = []
    for chunk in all_chunks:
        sim = cosine_similarity(query_embedding, chunk["embedding"])

        
        if sim >= MIN_SIMILARITY:
            scored.append((sim, chunk))

    print(f"found : {len(scored)}")
    top_matches = sorted(scored, key=lambda x: x[0], reverse=True)[:k]

    return [chunk["text"] for _, chunk in top_matches]

def load_cached_embeddings(cache_path:str):
    if not os.path.exists(cache_path):
        raise FileNotFoundError(f"No embeddings cache found at {cache_path}. Please run cache_embeddings.py first.")

    with open(cache_path, "rb") as f:
        all_chunks = pickle.load(f)

    #(f"Loaded {len(all_chunks)} chunks from cache.")
    return all_chunks
