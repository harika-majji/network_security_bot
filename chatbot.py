#!/usr/bin/env python3
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import chromadb
import os
import argparse
import time
from constants import CHROMA_SETTINGS

if not load_dotenv():
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

def initialize():
    embeddings_model_name = "all-MiniLM-L6-v2"
    #os.environ.get("EMBEDDINGS_MODEL_NAME")
    persist_directory = "db"
    #os.environ.get('PERSIST_DIRECTORY')

    model_type = "GPT4All" #os.environ.get('MODEL_TYPE')
    model_path = "models/ggml-gpt4all-j-v1.3-groovy.bin" #os.environ.get('MODEL_PATH')
    model_n_ctx = 1000 #os.environ.get('MODEL_N_CTX')
    model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
    target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))



def similarity_search(query, index):
    matched_docs = index.similarity_search(query, k=4)
    sources = []
    for doc in matched_docs:
        sources.append(
            {
                "page_content": doc.page_content,
                "metadata": doc.metadata,
            }
        )

    return matched_docs, sources
def initialize_llm(args):
    embeddings_model_name = "all-MiniLM-L6-v2"
    #os.environ.get("EMBEDDINGS_MODEL_NAME")
    persist_directory = "db"
    #os.environ.get('PERSIST_DIRECTORY')

    model_type = "GPT4All" #os.environ.get('MODEL_TYPE')
    model_path = "models/ggml-gpt4all-j-v1.3-groovy.bin" #os.environ.get('MODEL_PATH')
    model_n_ctx = 1000 #os.environ.get('MODEL_N_CTX')
    #model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
    target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',1))
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
    # Prepare the LLM
    print("Prepare the LLM")
    match model_type:
        case "LlamaCpp":
            llm = LlamaCpp(model_path=model_path, max_tokens=model_n_ctx, n_batch=model_n_batch, callbacks=callbacks, verbose=False)
        case "GPT4All":
            llm = GPT4All(model=model_path, max_tokens=model_n_ctx, backend='gptj', callbacks=callbacks , verbose=False)
        case _default:
            # raise exception if model_type is not supported
            raise Exception("Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")
    print("LLM created");
    return llm


def generateLLMResponse(llm, question, args):
    # Parse the command line arguments
    embeddings_model_name = "all-MiniLM-L6-v2"
    persist_directory = "db"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS , path=persist_directory)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS, client=chroma_client)
    retriever = db.as_retriever(search_kwargs={'k':1})
    template = """
                Use the following pieces of context to answer the question at the end.
                If you don't know the answer, just say that you don't know, don't try to make up an answer.
                Context: {context}
                .........
                Question: {question}
                Answer: Let's think step by step."""
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    #retriever = db.as_retriever(search_type="mmr", search_kwargs={'k': 2, 'lambda_mult': 0.5})

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, verbose=False , return_source_documents= not args.hide_source,chain_type_kwargs={"prompt": prompt })
    # Interactive questions and answers
    print(f"Lets ask the bot")
    res = qa(question)
    print("Result \n ",res)
    print("\nSimilarity ", db.similarity_search(question))
    #answer, docs = res['result'], [] if args.hide_source else res['source_documents']
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
