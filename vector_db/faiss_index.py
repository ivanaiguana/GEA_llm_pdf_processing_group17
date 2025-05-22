
import faiss
import numpy as np

def store_embeddings(chunks, embedding_fn):
    embeddings = [embedding_fn(chunk) for chunk in chunks]
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index, chunks

def search_index(query, index, chunks, embedding_fn, top_k=3):
    q_embed = np.array([embedding_fn(query)]).astype("float32")
    distances, indices = index.search(q_embed, top_k)
    return [chunks[i] for i in indices[0]]
