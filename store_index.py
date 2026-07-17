from dotenv import load_dotenv
import os

from src.helper import (
    load_pdf_files,
    filter_to_minimal_docs,
    text_split,
    download_embeddings
)

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

# Get Pinecone API Key
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in .env file")

# Load PDF files
extracted_data = load_pdf_files(data="data/")

# Keep only required metadata
filter_data = filter_to_minimal_docs(extracted_data)

# Split into chunks
text_chunks = text_split(filter_data)

# Load HuggingFace Embeddings
embedding = download_embeddings()

# Connect to Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Pinecone Index Name
index_name = "medical-chatbot"

# Create Index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

print("Pinecone Index Ready!")

# Upload documents to Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embedding,
    index_name=index_name
)

print("Documents uploaded successfully!")