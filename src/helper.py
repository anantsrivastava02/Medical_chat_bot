
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
def load_pdf(data):
    loader = DirectoryLoader(data , glob="*.pdf" , loader_cls= PyPDFLoader)
    document = loader.load()
    return document

def text_split(extracted):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500 , chunk_overlap = 20)
    text_chunk = text_splitter.split_documents(extracted)
    return text_chunk

def download_hugging_face_embedding():
    embeddings = HuggingFaceEmbeddings(model_name= "sentence-transformers/all-MiniLM-L6-v2")
    return embeddings