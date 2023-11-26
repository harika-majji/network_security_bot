from flask import Flask, render_template, request, jsonify
#from flask_cors import CORS
from chat import get_response
from chatbot import generateLLMResponse, parse_arguments,initialize_llm

app= Flask(__name__)
#CORS(app)

init_llm = None

def get_initialized_llm(parser):
    global init_llm
    if init_llm is None:
        init_llm = initialize_llm(parser)
    return init_llm

@app.get("/")
def render():
    return render_template("botScreen.html")

@app.post("/getAllTopics")
def getAllTopics():
    topicList = ["Public key cryptography", "Symmetric Encryption", "Block Cipher", "Stream Cipher", "Message Authentication"];
    message = {"topicList": topicList}
    return jsonify(message)

@app.post("/generateQuiz")
def generateQuiz():  
    topic = request.get_json().get("question")
    query = topic
    print(query)
    response = ""
    parser = parse_arguments()
    llm  = get_initialized_llm(parser);
    print("LLM retrieved")
    if(llm is not None):
        bot_response = generateLLMResponse(llm, query, parser,True)
        questions = bot_response['questions']
        answers = bot_response['answers']
        print("Questions",questions)
        print("answers",answers)
        citation = bot_response['source']
        response= {"answers": answers, 'questions':questions,"citation": citation}
    else:
        print("Failed");
        response = { "answer": "failure", "citation": ""}

    return jsonify(response)

@app.post("/generateChat")
def generateChat():
    
    query = request.get_json().get("question")
    result = get_response(query)
    response = ""
    if(result == "IDK"):
        parser = parse_arguments()
        llm  = get_initialized_llm(parser);
        print("LLM retrieved")
        if(llm is not None):
            bot_response = generateLLMResponse(llm, query, parser)
            answer, docs = bot_response['result'], [] if parser.hide_source else bot_response['source_documents']
            citation = docs[0].metadata["source"]
            response= {"answer": answer,"citation": citation}
        else:
            print("Failed");
            response = { "answer": "failure", "citation": ""}
    else:
        response = {"answer": result,"citation": ""}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
