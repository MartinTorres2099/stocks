import pymongo 
import nltk
import spacy
import streamlit as st

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["stocks_processed_data_db"]
collection = db["stocks_processed_data_collection"]

def query_db(query):
  results = collection.find(query)
  return results

def extract_entities(user_input):
  # Use Spacy to extract entities 
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(user_input)
  entities = [(ent.text, ent.label_) for ent in doc.ents]
  return entities

def get_response(user_input):

  entities = extract_entities(user_input)
  
  # Define lookup queries based on entities
  name_query = {"firstName": entities[0][0]} if "PERSON" in [x[1] for x in entities] else None

  date_query = {"txDate": entities[0][0]} if "DATE" in [x[1] for x in entities] else None

  # Query db
  results = query_db(name_query or date_query or {})
  
  if results:
    return "I found the following relevant information in my database: " + str(results)
  else:
    return "I'm sorry Dave, I'm afraid I can't do that."
  
  st.title("Stock Trade Chatbot")

user_input = st.text_input("Ask me a question about stock trades")

if user_input:
  response = get_response(user_input)
  st.text(response)
