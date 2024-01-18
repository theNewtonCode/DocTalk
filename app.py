import os
import shutil
from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
