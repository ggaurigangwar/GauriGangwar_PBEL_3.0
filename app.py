from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

from langchain_pinecone import PineconeVectorStore
from langchain_ollama import ChatOllama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from src.helper import download_hugging_face_embeddings
from src.prompt import *

app = Flask(__name__)

load_dotenv()

embedding = download_hugging_face_embeddings()


index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embedding
)


retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k":3}
)


llm = ChatOllama(
    model="llama3",
    temperature=0
)


question_answer_chain = create_stuff_documents_chain(
    llm,
    prompt
)

rag_chain = create_retrieval_chain(
    retriever,
    question_answer_chain
)


@app.route("/")
def home():
    return render_template("chat.html")


from flask import Response, stream_with_context

@app.route("/stream", methods=["POST"])
def stream():

    data = request.get_json()

    question = data["message"]

    def generate():

        for chunk in rag_chain.stream({

            "input": question

        }):

            if "answer" in chunk:

                yield chunk["answer"]

    return Response(

        stream_with_context(generate()),

        mimetype="text/plain"

    )

if __name__ == "__main__":
    app.run(debug=True)


