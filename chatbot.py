#!/usr/bin/env python3
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA, LLMChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import chromadb
import os
import re
import argparse
import time
from constants import CHROMA_SETTINGS

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

def initialize_llm(args):
    embeddings_model_name = "all-MiniLM-L6-v2"
    persist_directory = "db"

    model_type = "GPT4All"
    model_path = "models/ggml-gpt4all-j-v1.3-groovy.bin"
    model_n_ctx = 1000 
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
    # Prepare the LLM
    print("Prepare the LLM")
    llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gptj',temp = 0, callbacks=callbacks ,repeat_penalty = 1.15, verbose=False)
    print("LLM created")
    return llm


def generateLLMResponse(llm, question, args,quiz):
    # Parse the command line arguments
    embeddings_model_name = "all-MiniLM-L6-v2"
    persist_directory = "db"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS , path=persist_directory)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS, client=chroma_client)
    retriever = db.as_retriever(search_kwargs={'k':3})
    if(quiz):
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever , return_source_documents= not args.hide_source)
        # Interactive questions and answers
        print(f"Lets ask the bot")
        res = qa(question)
        print("Result \n ",res)
        documents = res['source_documents']
        document = ''
        for doc in documents:
            if(question.lower() in doc.page_content.lower()):
                document = doc.page_content
                
        pattern = '\[QUESTION\]\s*(.*?)\s*\[ANSWER\]:\s*(.*?)\s*\[SOURCE\]:\s*(.*?)\s*\[PAGE\]:\s*(\w+)'
        matches = re.findall(pattern, document, re.DOTALL)
        questionList = []
        answerList = []
        sourceList= []
        for question, answer, source, page in matches:
            questionList.append(question.strip())
            answerList.append(answer.strip())
            sourceList.append(source.strip() + " ,Page:" + page.strip())
        response ={'questions': questionList,'answers': answerList, 'source': sourceList }
        return response
    else:
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents= not args.hide_source)
        # Interactive questions and answers
        print(f"Lets ask the bot")
        res = qa(question)
        print("Result \n ",res)
    return res

def parse_arguments():
    parser = argparse.ArgumentParser(description='network_security_bot: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()


if __name__ == "__main__":
    generateLLMResponse(" What is entrophy" , parse_arguments());
