# Congressional Trading ChatBot

Hello everyone, this project aims to make a conversational chatbot on the trades made by our elected officials in Washington.
The information is public domain. By looking at publicialy available data I hope we can start looking at what,who,when, and why certain stocks were bought. A larger project will be to make the correlation between Congressional stock purchases/sales and look at laws that our elected officals are passing (or stoppping) and see if there is correlation between the two. This is purely for academic purposes and in no way intended to be used to make anyone accountable for their actions when creating/stopping legislation.

## POC Work
I was originally going to create a web scraper to pull the necessary data. After some failed attempts, I started looking at using an API call instead. I think the issue with the API code is the fact that the API information is not the same as the website data so the API code would need to be refactored to take into account how the API data is structured.

## Phase 1 - Information Gathering
Before I got too deep in the weeds in refactoring the API code, it dawned on me - what if I downloaded the website? I only need the HTML pages and nothing else. And that's what I did. Used a tool to copy the website locally. You can use any number of tools to automatically copy an entire website locally. Use the one that you are most familiar with. I now have thousands of HTML pages, each no more than 21KB in size with all the informaiton I need and then some. 

## Phase 2 - Parse the Data
With the data now acquired, I can parse the html data locally. I wrote some python code to parse the html files. It pulls out most of the fields I want to be able to use the Chatbot to interact with. There are a few fields I did not extract, not because I don't think they are useful, it would require additional coding to pull the data and at this point, I have enough relevant information to query. Here is a quick workflow of Phase 2: 

1. Place hmtl files in C:\git\sws\trades
2. Activate virtual environment: activate
3. Parse the data by running: python html_parser.py
4. This creates a file located here: C:\git\stocks\data\stocktrade.csv

As pages are updated on the website, all I need to do is follow the steps above to update the CSV file.

Some of the fields in the code were commented out because I wanted to move on with the project. It parses out most of the information I need and I may update the code later if I feel it is necessary for the Chatbot to have. 

## Phase 3 - Use LangChain to import data into a DB table

With the data parsed we can now use LangChain to save the data to a local mondoDB table. 

### Install pre-requasites
The following command will install langchain and streamlit needed to vectorize the data and interact with it:

```
pip install langchain streamlit pymongo transformers faiss-cpu sentence-transformers torch torchvision
pip install -U accelerate
pip3 install transformers>=4.32.0 optimum>=1.12.0
pip install --upgrade protobuf

nvcc --version
pip3 install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu114/
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
pip uninstall transformers
pip install transformers
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
python -c "import torch; print(torch.cuda.device_count())" 
pip install torch==1.13.1 -f https://download.pytorch.org/whl/cu122/torch_stable.html

Install NLM
   pip install nltk
   pip install spacy
   python -m spacy download en_core_web_sm
   pip install transformers

```
With the pre-requasites installed, we can write the code to to import the data into a mondodb table.

### Setup Local Environment

With the prerequasites installed, it is now time to setup the local environment.

1. Launch mondodb in a seperate CMD: C:\"Program Files"\MongoDB\Server\6.0\bin\mongod --port 27017 --dbpath C:\git\db
2. Laucnh MondoDBCompass app to verify MondoDB is running and view the new DB when it is created.
3. Launch Tika service in a seperate CMD: 
    a. CD C:\tika
    b. START /B java -jar tika-server-standard-2.8.0.jar --port 9998
4. Download the local model: python ./download_model.py
5. Inport the data by running: python import_csv_to_db.py
6. Process data by running process_data.py

### Run Application

With the local environment running, run the following command to start the application:

python main.py

Command to test code:
streamlit run import_data.py

Manual build:
1. html_parser.py
2. import_csv_to_db.py
3. chunk_stocks_db.py
4. streamlit run chat_bot.py

### Troubleshooting
If you get this error:
ImportError: cannot import name 'builder' from 'google.protobuf.internal' (C:\git\stocks\venv\lib\site-packages\google\protobuf\internal\__init__.py)
Run the following:
pip uninstall protobuf
pip install protobuf

### Current issues
The code runs, it only brings back a very small chunk of data. I want the chatbot to answer questions regarding the following:
1. When a stock purchase/sale was executed
2. Stock price at the time of sale (not coded yet)
3. Current stock price (not coded yet)
4. Time of the reported purchase/sale of the stock compared to the actual date of the purchase/sale (how many days between them)
5. Stock price at original purchase/sale and price at the time of reporting and current price
6. The amount of stock involved
7. Report on profit or loss
8. Who made the purchase - government official or family member

Since this is a POC it is running on a local model. Is there a good model that I can use to run these types of queries?
Should I change how I'm accessing the data? Maybe change the chunk size? Store it in a different manner? 
Maybe train the model on the data instead of querying the DB? I'm open to suggestions.