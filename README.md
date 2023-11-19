Welcome to Network_Security_Bot
<h2> Project Description </h2>
<p>Our task is to build a quiz bot based on a network security course using the open-source alternatives to ChatGPT that can be run on any local machine. As data privacy can be compromised when sending data over the internet, it is mandatory to keep it on local system. The bot offers two types of questions: randomly generated questions and specific topic questions, the answers should be pulled from the network security database. The bot is trained using network security quizzes, lecture slides, network security textbook, and the Internet. The quiz includes multiple-choice questions, true/false questions, and open-ended questions. Finally, the bot will provide feedback on the user's answers if it is correct or not along with the reference source documentation title.</p>
<h2> Documentation </h2>
<h2> System Architecture </h2>
<h2> Video </h2> 
<h2> Prerequisite </h2>
Install python3
Create virtual environment
python3 -m venv venv
venv/bin/activate - for MAC users
venv/Scripts/activate - for WINDOWS users
<h2> Requirements </h2>
*pip install langchain==0.0.274</br>
*pip install gpt4all==1.0.8</br>
*pip install chromadb==0.4.7</br>
*pip install llama-cpp-python==0.1.81</br>
*pip install urllib3==2.0.4 </br>
*pip install PyMuPDF==1.23.1 </br>
*pip install python-dotenv==1.0.0 </br>
*pip install unstructured==0.10.8 </br>
*pip install extract-msg==0.45.0</br>
*pip install tabulate==0.9.0</br>
*pip install pandoc==2.3 </br>
*pip install pypandoc==1.11 </br>
*pip install pypdfcd</br>
*pip install tqdm==4.66.1</br>
*pip install sentence_transformers==2.2.2 </br>
*pip install flask


Download model from : https://drive.google.com/file/d/1RHfTHIZ8-N3FV4Lj_m99NYq8D4lOqgtM/view?usp=drive_link and create a model folder and add it.

<h2> Step by step instructions for executions </h2>

•	python train.py  # only once when the application runs Quote break.</br>
•	python ingest.py # only once until the db folder is generated with all the training data </br>
•	python app.py    # execute this command to run the application

<h2> Features </h2>
<h2> Describe training data and data formats </h2>

