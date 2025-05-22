
import openai
import os

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_version = "2023-05-15"

def get_embedding(text, deployment="text-embedding-ada-002"):
    response = openai.Embedding.create(
        input=text,
        engine=deployment
    )
    return response["data"][0]["embedding"]
