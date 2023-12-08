import streamlit as st
import pymongo
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import faiss
import numpy as np
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
source_db = client["stocks_processed_data_db"]
source_collection = source_db["stocks_processed_data_collection"]

# Load the local language model
model_path = "stable-vicuna-13B.ggml.q4_2.bin"
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained(model_path)

# FAISS setup for fast similarity search
faiss_index = faiss.IndexFlatIP(768)  # Assuming the model has 768 dimensions

def save_chat_to_mongodb(question, response):
    chat_document = {
        "question": question,
        "response": response,
    }
    chat_collection = source_db["stocks_chat_collection"]
    chat_collection.insert_one(chat_document)



def answer_question(question):
    # Search for similar documents in MongoDB using FAISS
    question_embedding = model.encode(question)
    question_embedding = np.expand_dims(question_embedding, axis=0).astype('float32')
    D, I = faiss_index.search(question_embedding, k=1)

    if D[0][0] < 0.2:  # You can adjust the threshold as needed
        similar_document = source_collection.find_one({"_id": I[0][0]})
        return similar_document["content"]
    else:
        return "I'm sorry Dave, I'm afraid I can't do that."

# Streamlit app
def main():
    st.title("Chatbot for Stock Data")

    st.sidebar.title("Chat Options")
    chat_history = st.sidebar.checkbox("Save Chat History")
    save_to_mongodb = st.sidebar.checkbox("Save to MongoDB")

    if not chat_history:
        st.warning("Chat history is disabled. Enable 'Save Chat History' to save chats.")
    else:
        local_save = st.sidebar.checkbox("Save Locally")
        if local_save:
            local_file_path = st.text_input("Enter local file path:")
            question = st.text_input("Ask me a question:")
            if st.button("Ask"):
                response = answer_question(question)
                st.write("Chatbot: ", response)

                if save_to_mongodb:
                    # Save the chat to MongoDB
                    save_chat_to_mongodb(question, response)
                if local_file_path:
                    # Save the chat to the specified local file
                    save_chat_to_file(question, response, local_file_path)
        else:
            question = st.text_input("Ask me a question:")
            if st.button("Ask"):
                response = answer_question(question)
                st.write("Chatbot: ", response)

                if save_to_mongodb:
                    # Save the chat to MongoDB
                    save_chat_to_mongodb(question, response)

def save_chat_to_file(question, response, file_path):
    with open(file_path, "a") as chat_file:
        chat_file.write(f"User: {question}\n")
        chat_file.write(f"Chatbot: {response}\n\n")


if __name__ == "__main__":
    main()
