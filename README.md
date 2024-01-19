# DocTalk - Offline Document Question-Answering Application

DocTalk is an offline document question-answering application developed with Flask, LangChain, LaMini, and ChromaDB. This cost-free solution enables users to process PDF documents, generate embeddings, and perform question-answering tasks without relying on external APIs.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Application Workflow](#application-workflow)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

DocTalk integrates several technologies to provide an offline document question-answering system. Users can upload PDFs, process them, and seek answers using a pre-trained LaMini model. The application's modular structure ensures flexibility and ease of use.

## Repository Structure

1. **docs:** Contains PDF files uploaded by users for processing.
2. **LaMini-T5-738M:** Holds the LaMini model. Users need to download it using Git LFS commands before running the application.
3. **static:** Contains CSS, design elements, and JavaScript script files.
4. **templates:** Holds HTML files for the user interface design.
5. **vector_db_main:** Users need to create an empty folder named `vector_db_main` to store the ChromaDB vector database.

## Application Workflow

1. **User Interaction:**
   - Users drag and drop PDF files onto the home page.
   - The application checks for existing files and an empty vector database.

2. **Initialization:**
   - If existing files or data are found, the application clears the `vector_db_main` folder and the `docs` folder.

3. **Processing PDFs:**
   - Clicking the 'Learn' button triggers the processing of the uploaded PDF.
   - Processing involves tokenization, chunking, embeddings generation using LaMini, and storing embeddings in the ChromaDB vector database.

4. **Question-Answering:**
   - After processing, users click the 'Start' button to navigate to the QA page.
   - The application utilizes functions from `qa_app.py` for question-answering using the preprocessed embeddings and the vector database.

## Setup Instructions

To run the application:

1. Create a virtual environment for better isolation.
2. Clone the repository: `git clone https://github.com/theNewtonCode/DocTalk.git`.
3. Install necessary libraries from `requirements.txt`.
4. Create an empty folder named `vector_db_main` in the project directory.
5. Download the LaMini model using Git LFS commands:
   ```bash
   git lfs install
   git clone https://huggingface.co/MBZUAI/LaMini-T5-738M
   ```
6. Run the application by executing `app.py`.

## Usage

1. Drag and drop PDF files onto the home page.
2. Click the 'Learn' button to process the PDF and store embeddings.
3. Click the 'Start' button to navigate to the QA page and seek answers.

## Contributing

Contributions are welcome! Please check the [contribution guidelines](CONTRIBUTING.md) before getting started.

## License

This project is licensed under the [MIT License](LICENSE).
