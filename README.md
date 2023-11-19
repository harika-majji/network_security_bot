Welcome to Network_Security_Bot
<h2> Project Description </h2>
<h2> Documentation </h2>
<h2> System Architecture </h2>
<p align="center">
  <img src="System Architecture.png" width="350" title="sys arch">
</p>
<p>
  <b>User Input:</b></br>
  The user enters a prompt in the user interface.</br>
  <b>Embedding Generation:</b></br>
  The system converts user queries into numerical embeddings, capturing the meaning of the text.</br>
  <b>Vector Database Query:</b></br>
  The application sends the generated embedding to the vector database.</br>
  The vector database compares the user's embedding with precomputed embeddings of various documents.</br>
  It returns a list of documents that are most relevant to the user's prompt based on the similarity of their embeddings to the user's embedding.</br>
  <b>Contextual Prompt Creation:</b></br>
  The application creates a new prompt by combining the user's initial prompt with the retrieved documents as context.</br>
  This step aims to provide additional information and context to the local Language Model.</br>
  <b>Local Language Model Processing (LLM):</b></br>
  The modified prompt, containing both the user's input and relevant context documents, is sent to the local Language Model (LLM).</br>
  The LLM processes the contextual prompt and generates a response based on the combined information.</br>
  The response includes citations or references from the context documents, demonstrating the sources used to generate the answer.</br>
  <b>User Interface Display:</b></br>
  The system presents the response along with citations in the user interface.
  Users can view the answer and sources, ensuring transparency and credibility in the information provided.
</p>
<h2> Video </h2> 
<h2> Prerequisite </h2>
Install python3
Create virtual environment
python3 -m venv venv
venv/bin/activate - for MAC users
venv/Scripts/activate - for WINDOWS users
<h2> Requirements </h2>
*pip install langchain==0.0.274 
*pip install gpt4all==1.0.8 
*pip install chromadb==0.4.7 
*pip install llama-cpp-python==0.1.81
*pip install urllib3==2.0.4 
*pip install PyMuPDF==1.23.1 
*pip install python-dotenv==1.0.0 
*pip install unstructured==0.10.8 
*pip install extract-msg==0.45.0
*pip install tabulate==0.9.0
*pip install pandoc==2.3 
*pip install pypandoc==1.11 
*pip install pypdfcd
*pip install tqdm==4.66.1
*pip install sentence_transformers==2.2.2 
*pip install flask


Download model from : https://drive.google.com/file/d/1RHfTHIZ8-N3FV4Lj_m99NYq8D4lOqgtM/view?usp=drive_link and create a model folder and add it.

<h2> Step by step instructions for executions </h2>

•	python train.py  # only once when the application runs
Quote break.
•	python ingest.py # only once until the db folder is generated with all the training data
•	python app.py    # execute this command to run the application

<h2> Features </h2>
<h2> Describe training data and data formats </h2>

