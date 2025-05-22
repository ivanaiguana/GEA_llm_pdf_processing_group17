
from ocr.azure_ocr import extract_text_from_pdf
from parser.chunker import chunk_text
from embedding.embedder import get_embedding
from vector_db.faiss_index import store_embeddings, search_index
from rag_pipeline.ask import ask_gpt

def run_pipeline(pdf_path, question):
    print("Extracting text...")
    text = extract_text_from_pdf(pdf_path)

    print("Chunking text...")
    chunks = chunk_text(text)

    print("Generating embeddings...")
    index, stored_chunks = store_embeddings(chunks, get_embedding)

    print("Searching...")
    relevant_chunks = search_index(question, index, stored_chunks, get_embedding)

    print("Asking GPT...")
    answer = ask_gpt(relevant_chunks, question)

    print("Answer:", answer)
    return answer

if __name__ == "__main__":
    run_pipeline("sample.pdf", "What is the function of the COROS OP5?")
