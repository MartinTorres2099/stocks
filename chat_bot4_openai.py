import pymongo
import streamlit as st

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
source_db = client["stocks_processed_data_db"]
source_collection = source_db["stocks_processed_data_collection"]

# Function to query MongoDB
def query_mongodb(query):
    result = source_collection.find_one({"text": query})
    if result:
        return result
    else:
        return "I'm sorry Dave, I'm afraid I can't do that."

# Streamlit UI
st.title("Stocks Chatbot")
user_input = st.text_input("Ask a question:")
if user_input:
    response = query_mongodb(user_input)
    st.text(response)

# Save chat history
if st.button("Save Chat History"):
    # Implement code to save chat history to a file
