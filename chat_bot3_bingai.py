import pymongo
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import streamlit as st
import spacy
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
source_db = client["stocks_processed_data_db"]
source_collection = source_db["stocks_processed_data_collection"]

# Load a Spacy model (you might need to download it first with "python -m spacy download en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

# Load Language Model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('C:\\git\\stocks\\stable-vicuna-13B.ggml.q4_2.bin')

def query_mongodb(question):
    # Use Spacy for Named Entity Recognition
    doc = nlp(question)
    
    # This is just a placeholder and should be replaced with actual parsing logic
    query = {}
    for ent in doc.ents:
        if ent.label_ == "ORG" and "issuerName" not in query:  # If the entity is an organization, it might be the issuerName
            query["issuerName"] = ent.text
        # Add more conditions for other table headers and entity types...
    
    results = source_collection.find(query)
    return results

def generate_response(results):
    if results.count() > 0:
        result = results[0]  # Use the first result for simplicity
        # Encode input context
        input_context = ' '.join([f"{key}: {value}" for key, value in result.items() if key != '_id'])
        input_ids = tokenizer.encode(input_context, return_tensors='pt')

        # Generate response
        output = model.generate(input_ids, max_length=150, temperature=0.7, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    else:
        response = "I'm sorry Dave, I'm afraid I can't do that."
    
    return response

# Streamlit App
st.title('My Chatbot')
user_input = st.text_input("Ask something:")
if st.button('Submit'):
    results = query_mongodb(user_input)
    response = generate_response(results)
    st.write(response)
