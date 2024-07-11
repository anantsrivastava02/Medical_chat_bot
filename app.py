from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embedding
from src.prompt import *
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone as PineconeStore 
import pinecone 
from langchain.llms import ctransformers
from langchain import prompts
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
KEY = os.getenv("PINECONE_API_KEY")

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
docsearch = PineconeStore.from_existing_index(index_name= index_name , embedding=embeddings)

prompt1 = PromptTemplate(template=prompt , input_variables=["context" , "question"])
chain_type_kwargs = {"prompt":prompt1}

from langchain_community.llms import CTransformers
llm = CTransformers(
        model = "C:/Users/anant/deep learning/Medical_chat_bot/model/llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        config={'max_new_tokens':512,'temperature':0.8}
    )

qa = RetrievalQA.from_chain_type(
    llm= llm,
    chain_type = "stuff",
    retriever = docsearch.as_retriever(search_kwargs ={'k' : 2}),
    return_source_documents = True,
    chain_type_kwargs = chain_type_kwargs
)


@app.route("/")
def index():
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)