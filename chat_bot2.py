import streamlit as st
import pymongo
import faiss
# import numpy as np
import chromadb
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
# from constants import CHROMA_SETTINGS
# from config import PERSIST_DIRECTORY

# os.environ['PERSIST_DIRECTORY'] = '/c/git/stocks'
# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
source_db = client["stocks_processed_data_db"]
source_collection = source_db["stocks_processed_data_collection"]

# Load the local language model for chatbot
chatbot_model_name_or_path = "/git/stocks/"
chatbot_model = AutoModelForCausalLM.from_pretrained(chatbot_model_name_or_path, device_map="auto", trust_remote_code=False, revision="main")
chatbot_tokenizer = AutoTokenizer.from_pretrained(chatbot_model_name_or_path, use_fast=True)

# FAISS setup for fast similarity search
faiss_index = faiss.IndexFlatIP(768)  # Assuming the model has 768 dimensions

# Langchain setup for QA
embeddings_model_name = os.environ.get("stable-vicuna-13B.ggml.q4_2.bin")  # Replace with your model name
# if 'PERSIST_DIRECTORY' not in os.environ:
#    os.environ['PERSIST_DIRECTORY'] = '/c/git/stocks'
# persist_directory = os.environ(PERSIST_DIRECTORY)
model_type = "LlamaCpp"  # Change this to the desired model type (LlamaCpp or GPT4All)
qa_model_path = "/git/stocks/"  # Replace with your QA model path
qa_model_n_ctx = 1024  # Adjust the context length as needed
qa_model_n_batch = 8  # Adjust the batch size as needed
target_source_chunks = 4  # Adjust the target source chunks as needed

# Streamlit app
def main():
    st.title("Chatbot for Congressional Stock Trades")

    st.sidebar.title("Chat Options")
    chat_history = st.sidebar.checkbox("Save Chat History")
    save_to_mongodb = st.sidebar.checkbox("Save to MongoDB")

    question = st.text_input("Ask me a question:")
    if st.button("Ask"):
        # Answer the question using the chatbot model
        chatbot_response = answer_question(question)
        st.write("Chatbot: ", chatbot_response)

        # Perform QA using the Langchain model
        qa_response = perform_qa(question)
        st.write("QA Model: ", qa_response)

        if chat_history:
            if save_to_mongodb:
                # Save the chat to MongoDB
                save_chat_to_mongodb(question, chatbot_response, qa_response)
            else:
                # Save the chat to a local file (implement as needed)
                save_chat_to_file(question, chatbot_response, qa_response)

# Answer a question using the chatbot model
def answer_question(question):
    prompt_template = f'''[INST] <<SYS>>
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
    <</SYS>>
    {question}[/INST]

    '''

    input_ids = chatbot_tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = chatbot_model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=512)
    generated_response = chatbot_tokenizer.decode(output[0])

    return generated_response

# Perform QA using the Langchain model
def perform_qa(question):
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    # chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=persist_directory)
    # db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS, client=chroma_client)
    # retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})

    # Choose the LLM type based on model_type and create the RetrievalQA object
    llm = None
    if model_type == "LlamaCpp":
        llm = LlamaCpp(model_path=qa_model_path, max_tokens=qa_model_n_ctx, n_batch=qa_model_n_batch, verbose=False)
    elif model_type == "GPT4All":
        llm = GPT4All(model=qa_model_path, max_tokens=qa_model_n_ctx, backend='gptj', n_batch=qa_model_n_batch, verbose=False)
    else:
        raise Exception(f"Model type {model_type} is not supported. Please choose one of the following: LlamaCpp, GPT4All")

    # qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    # res = qa(question)
    # qa_response = res['result']

    #return qa_response

# Save the chat to MongoDB
def save_chat_to_mongodb(question, chatbot_response, qa_response):
    chat_document = {
        "question": question,
        "chatbot_response": chatbot_response,
        "qa_response": qa_response,
    }
    chat_collection = source_db["stocks_chat_collection"]
    chat_collection.insert_one(chat_document)

# Save the chat to a local file (implement as needed)
def save_chat_to_file(question, chatbot_response, qa_response, file_path):
    # Implement the code to save the chat to a local file here
    with open(file_path, "a") as chat_file:
        chat_file.write(f"User: {question}\n")
        chat_file.write(f"Chatbot: {chatbot_response}\n\n")
        chat_file.write(f"Chatbot QA: {qa_response}\n\n\n")
    pass

if __name__ == "__main__":
    main()