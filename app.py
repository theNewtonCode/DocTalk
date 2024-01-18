import os
import shutil
from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 
from transformers import pipeline
import torch 
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.embeddings import SentenceTransformerEmbeddings 
from langchain.vectorstores import Chroma 
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA 
from qa_app import process_answer
import random


app = Flask(__name__)


device = torch.device('cpu')

checkpoint = "LaMini-T5-738M"

# print(f"Checkpoint path: {checkpoint}")  
# tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# base_model = AutoModelForSeq2SeqLM.from_pretrained(
#     checkpoint,
#     torch_dtype=torch.float32
# )


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and file.filename.endswith('.pdf'):
        # Remove existing files from the 'docs' folder
        docs_folder = 'docs'
        for existing_file in os.listdir(docs_folder):
            existing_file_path = os.path.join(docs_folder, existing_file)
            try:
                if os.path.isfile(existing_file_path) or os.path.islink(existing_file_path):
                    os.unlink(existing_file_path)
                elif os.path.isdir(existing_file_path):
                    shutil.rmtree(existing_file_path)
            except Exception as e:
                print(f"Failed to delete {existing_file_path}. Reason: {e}")

        # Remove the contents of the 'vector_db_main' folder
        vector_db_main_folder = 'vector_db_main'
        for filename in os.listdir(vector_db_main_folder):
            file_path = os.path.join(vector_db_main_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

        # Save the file to the 'docs' folder
        file_path = os.path.join(docs_folder, file.filename)
        file.save(file_path)
        return 'File uploaded successfully'
    else:
        return 'Invalid file format. Please upload a PDF file.'
    
@app.route('/ask-doc')
def ask_doc():
    try:
        for root, dirs, files in os.walk("docs"):
            for file in files:
                if file.endswith(".pdf"):
                    print(file)
                    loader = PyPDFLoader(os.path.join(root, file))
        documents = loader.load()
        print("splitting into chunks")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        # create embeddings here
        print("Loading sentence transformers model")
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        # create vector store here
        print(f"Creating embeddings. May take some minutes...")

        db = Chroma.from_documents(texts, embeddings, persist_directory="vector_db_main")

        print(f"Ingestion complete! You can now run privateGPT.py to query your documents")
        return 'Document processed successfully'
    except Exception as e:
        print(f"Error processing document: {e}")
        return 'Error processing document'


@app.route('/lets-qa', methods=['POST', 'GET'])
def lets_qa():
    if request.method == 'POST':
        question = request.form['question']
        answer = process_answer(question)


        # Define a list of alternative texts
        alternative_texts = [
            "Happy to assist! Let me know if you have any other questions. 😊",
            "My pleasure! I hope the information I provided was insightful. 😉",
            "That's just a starting point! Ask more to learn more about this topic. 😙"
        ]

        random_text = random.choice(alternative_texts)
        answer = "Here is the information you requested. "+ answer + " " + random_text

        return render_template('lets_qa.html', question=question, answer=answer)
    else:
        return render_template('lets_qa.html', question="", answer="")


if __name__ == '__main__':
    app.run(debug=True)
