from src.helper import load_pdf , download_hugging_face_embedding , text_split
from langchain.vectorstores import Pinecone as PineconeStore
import pinecone
from dotenv import load_dotenv
import os 

load_dotenv()

# Get the API key from the environment variable
KEY = os.getenv("PINECONE_API_KEY")

extracted = load_pdf("data/")
test_chunks = text_split(extracted)
embeddings = download_hugging_face_embedding()

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec


pc = Pinecone(api_key=KEY)
index_name = "medicalchat"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    ) 

docsearch = PineconeStore.from_existing_index(index_name , embeddings)