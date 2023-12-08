I'm trying to build a chatbot to interact with data that has been parsed and placed into a mondodb database. The enviornment is a Windows 10 using a python virtual environment . The python code is stored here:
C:\git\stocks
The mondodb settings are as follows:
client = pymongo.MongoClient("mongodb://localhost:27017/")
source_db = client["stocks_processed_data_db"]
source_collection = source_db["stocks_processed_data_collection"]
The data in the mondodb was vectorized with langchain and then input into the db.
I want to use a local LLM (C:\git\stocks\stable-vicuna-13B.ggml.q4_2.bin) as the chatbot to interact with the mondodb data.
I want to use streamlit to create a website where users can input questions about the data and receive a response.
I want to be able to give the users the ability to save the data/chat history locally.
I only want the chatbot to answer questions that can be pulled from the mondodb collection, I do not want it to hillucinate. If an asnwer cannot be found from querying the mondodb collection I want the chatbot to respond with "I'm sorry Dave, I'm afraid I can't do that."
I want to use Natural Language Processing (NLP) libraries like NLTK, Spacy, or even transformers to extract relevant information from the user’s questions.
The mondodb currently has 5,122 entries, each with the data structure as follows:
{
  "_id": {
    "$oid": "651c3b126e064b389099ef51"
  },
  "text": "BITCOIN $BTC Cynthia Lummis bought $75000 of BITCOIN ($BTC) on 2021-08-16. She filed the trade after 52 days. 2021-10-09T00:00:00Z buy 50K–100K 52.0 2021-10-07 2021-08-16 nan female Cynthia Lummis republican self senate nan https://efdsearch.senate.gov/search/view/ptr/1124fac7-7277-4328-8740-fbaceeaac1b5/ Exchange/Platform: River"
{
  "_id": {
    "$oid": "651c3b126e064b389099ef52"
  },
  "text": "Construction Partners Inc ROAD:US Mark Warner sold $75000 of Construction Partners Inc (ROAD:US) on 2021-10-14. He filed the trade after 34 days. 2021-11-19T00:00:00Z sell 50K–100K 34.0 2021-11-17 2021-10-14 nan male Mark Warner democrat self senate nan https://efdsearch.senate.gov/search/view/ptr/1abf71df-3cf3-47b5-9f8f-16ca358a157e/ Shares received from SunTx Fulcrum Fund, L.P. - Construction Partners, Inc. (dba SunTx CPI Growth Company, Inc.)"
}
{
  "_id": {
    "$oid": "651c3b126e064b389099ef53"
  },
  "text": "W L GORE \\u0026 ASSOCIATES INC nan Chris Coons sold $8000 of W L GORE & ASSOCIATES INC on 2021-11-09. He filed the trade after 20 days. 2021-12-01T00:00:00Z sell 1K–15K 20.0 2021-11-29 2021-11-09 nan male Christopher Coons democrat child senate nan https://efdsearch.senate.gov/search/view/ptr/36b58614-d07b-408b-8ff9-b5846cbe801d/ Gorfam Inc. sold stock to benefit another shareholder. Child received only funds to cover taxes."
}
etc.
The answers can only come from the following data headers:
issuerName	issuerTicker	txType	tradeValue	reportingGap	Description	pubDate	filingDate	txDate	value	gender	firstName	lastName	party	owner	chamber	price	filingURL	comment
All of the data pertains to stock trades. What query logic should be used for questions and responses?
Do you require any more information so you can show and explain the steps needed to create the chatbot? And then show the completed python code at the end?

What are some complex NLP techniques and MongoDB queries that the users may ask if the data is based off of these fields only:
issuerName	issuerTicker	txType	tradeValue	reportingGap	Description	pubDate	filingDate	txDate	value	gender	firstName	lastName	party	owner	chamber	price	filingURL	comment
complex NLP techniques and MongoDB queries for stock trade data using issuerName, issuerTicker, txType, tradeValue, reportingGap, Description, pubDate, filingDate, txDate, value, gender, firstName, lastName, party, owner, chamber, price, filingURL, and comment fields
Answer | gpt-4 Model

Given the fields in your data, users might ask complex questions that require advanced NLP and MongoDB techniques. Here are some examples:

    Questions involving temporal analysis: Users might ask questions like "What was the total tradeValue of stocks bought by Democrats in the last quarter?". To answer such questions, you'd need to parse the time-related phrase ("in the last quarter") and convert it into a format that can be used in a MongoDB query. You might also need to handle different time formats and time zones.

    Questions involving entity relationships: Users might ask questions like "Who are the top 5 issuers in terms of tradeValue?". To answer this, you'd need to group the data by 'issuerName' and sum the 'tradeValue', then sort the results and limit the output to 5. In MongoDB, you can accomplish this using the $group, $sum, $sort, and $limit aggregation operators stackoverflow.com.

   pipeline = [
       {"$group": {"_id": "$issuerName", "totalTradeValue": {"$sum": "$tradeValue"}}},
       {"$sort": {"totalTradeValue": -1}},
       {"$limit": 5}
   ]
   results = source_collection.aggregate(pipeline)

    Questions involving text search: Users might ask questions like "Find all trades involving Bitcoin". To answer this, you'd need to use MongoDB's text search capabilities. First, create a text index on the 'text' field, then you can use the $text operator to search the text digitalocean.com.

   source_collection.create_index([("text", "text")])
   query = {"$text": {"$search": "Bitcoin"}}
   results = source_collection.find(query)

    Questions involving comparison of different fields: Users might ask questions like "Find all trades where the reportingGap is more than 30 days". To answer this, you'd need to use MongoDB's comparison query operators digitalocean.com.

   query = {"reportingGap": {"$gt": 30}}
   results = source_collection.find(query)

Remember, these are just examples. The actual questions users might ask will depend on the nature of your data and the types of insights users are interested in. You might need to use other NLP techniques and MongoDB operators to handle different types of questions.

Can you provide more examples of text search queries that can be performed on the data?
text search queries in MongoDB using Python
Answer | gpt-4 Model

Considering the fields in your data, here are some examples of text search queries that you might want to perform:

    Search for a single word: If you want to find all entries where a particular word appears, you can use the $text operator. For instance, to find all entries related to "Bitcoin", you can use:

    query = {"$text": {"$search": "Bitcoin"}}
    results = source_collection.find(query)
    ```

This will return all the documents that contain the term "Bitcoin" in the indexed fields mongodb.com.

    Case sensitive search: If you want your search to be case sensitive, you can use the $caseSensitive option. For example, to find all entries where the exact term "Bitcoin" (with a capital 'B') appears, you can use:

    query = {"$text": {"$search": "Bitcoin", "$caseSensitive": true}}
    results = source_collection.find(query)
    ```

This will return all the documents that contain the exact term "Bitcoin" (with a capital 'B') mongodb.com.

    Search for a phrase: If you want to search for an exact phrase, you can enclose the phrase in double quotes. For instance, to find all entries where the exact phrase "Bitcoin trade" appears, you can use:

    query = {"$text": {"$search": "\"Bitcoin trade\""}}
    results = source_collection.find(query)
    ```

This will return all the documents that contain the exact phrase "Bitcoin trade" mongodb.com.

    Negate a term: If you want to exclude documents that contain a particular term, you can prefix the term with a minus sign. For instance, to find all entries related to "Bitcoin" but not "trade", you can use:

    query = {"$text": {"$search": "Bitcoin -trade"}}
    results = source_collection.find(query)
    ```

This will return all the documents that contain the term "Bitcoin" but do not contain the term "trade" mongodb.com.

    Diacritic sensitive search: If you want your search to be sensitive to diacritics, you can use the $diacriticSensitive option. For instance, to find all entries where the exact term "résumé" appears, you can use:

    query = {"$text": {"$search": "résumé", "$diacriticSensitive": true}}
    results = source_collection.find(query)
    ```

This will return all the documents that contain the exact term "résumé" with the accent mongodb.com.

Remember, to use MongoDB's text search capabilities, you first need to create a text index on the fields you want to search. You can create a text index using the create_index method:

source_collection.create_index([("text", "text")])

This will create a text index on the 'text' field, allowing you to perform text search queries on this field mongodb.com.