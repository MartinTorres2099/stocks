import spacy
import streamlit as st
import nltk
from transformers import *

nlp = spacy.load('en_core_web_sm')
def extract_entities(question):
    doc = nlp(question)
    entities = {ent.label_: ent.text for ent in doc.ents}
    return entities
```
def query_db(entities):
    query = {k: v for k, v in entities.items() if k in ['issuerName', 'issuerTicker', 'txType', ...]}
    results = source_collection.find(query)
    return results
```
def generate_response(results):
    if results.count() > 0:
        # Generate response using your local LLM
        response = ...
    else:
        response = "I'm sorry Dave, I'm afraid I can't do that."
    return response
```
st.title('Stocks Chatbot')
user_input = st.text_input("Enter your question here:")
if st.button('Ask'):
    entities = extract_entities(user_input)
    results = query_db(entities)
    response = generate_response(results)
    st.write(response)
    ```
chat_history = []

# When the 'Ask' button is pressed
question = user_input
response = generate_response(results)
chat_history.append({'question': question, 'response': response})

# When the 'Download chat history' button is pressed
if st.button('Download chat history'):
    df = pd.DataFrame(chat_history)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="chat_history.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)
