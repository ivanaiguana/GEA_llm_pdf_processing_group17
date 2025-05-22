from azure.storage.blob import BlobServiceClient
import os
import fitz
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;t"
CONTAINER_NAME = "ivana-jiahao-ben"
PDF_PREFIX = "raw-pdfs/"

def extract_text_from_pdfs():
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    texts = []
    for blob in container_client.list_blobs():
        if blob.name.endswith(".pdf"):
            download_path = f"./tmp/{blob.name}"
            os.makedirs(os.path.dirname(download_path), exist_ok=True)
            with open(download_path, "wb") as f:
                f.write(container_client.download_blob(blob).readall())

            doc = fitz.open(download_path)
            text = "\n".join([page.get_text() for page in doc])
            texts.append({"filename": blob.name, "text": text})
    return texts

def extract_and_index():
    docs = extract_text_from_pdfs()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = []
    for doc in docs:
        splits = splitter.split_text(doc["text"])
        for s in splits:
            split_docs.append(Document(page_content=s, metadata={"source": doc["filename"]}))

    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.from_documents(split_docs, embeddings)
    vectordb.save_local("rag_index")

def ask_question(query):
    vectordb = FAISS.load_local("rag_index", OpenAIEmbeddings())
    retriever = vectordb.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=retriever)
    return qa.run(query)
