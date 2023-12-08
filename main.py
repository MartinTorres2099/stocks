import langchain
import streamlit as st
from langchain.llms import LlamaCpp
from langchain.chains import ConversationChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pymongo
import archive.chatbot as chatbot
import archive.process_data as process_data

# Fix for some new weird "no attribute 'verbose'" bug https://github.com/hwchase17/langchain/issues/4164
langchain.verbose = False
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

model_path = "./stable-vicuna-13B.ggml.q4_2.bin"

# Initialize LangChain
llm = LlamaCpp(
    model_path=model_path,
    # stop=["### Human:"],
    callback_manager=callback_manager,
    verbose=True,
    n_ctx=2048,
    n_batch=512,
)

# Use Sentence Transformers embeddings
embeddings = OpenAIEmbeddings(model_name="all-MiniLM-L6-v2")
chatchain = ConversationChain(llm=llm, embeddings=embeddings, prompt="Welcome to the congressional stock-trading chatbot")

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["stocks_db"]
collection = db["stocks_collection"]

# Streamlit web application
st.title("Congressional Chatbot")

user_input = st.text_input("Ask me anything relationg to congressional stock trades:")

if user_input:
    # Search the database for user input
    data = collection.find({"$text": {"$search": user_input}})

    # If data is found, process and generate a response
    if data.count() > 0:
        # Process and analyze the data as needed
        processed_data = [item['text'] for item in data]
        response = process_data.process_data(processed_data)

        # Generate a response based on processed data using the chatbot module
        chatbot_response = chatbot.generate_response(response)
        st.write("Chatbot:", chatbot_response)
    else:
        # If no data is found, provide the default response
        st.write("Chatbot: I'm sorry Dave, I'm afraid I can't do that.")

