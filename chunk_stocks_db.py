import pymongo
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
source_db = client["stocks_db"]
source_collection = source_db["stocks_collection"]

destination_db = client["stocks_processed_data_db"]
destination_collection = destination_db["stocks_processed_data_collection"]

# Define LangChain components
model = SentenceTransformer('all-MiniLM-L6-v2')
text_splitter = CharacterTextSplitter(
    separator=",",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

# Define LangChain process function
def langchain_process(text):
    # Split text into chunks using text_splitter
    chunks = text_splitter.split_text(text)  # Use the 'split' method
    
    # Process and store each chunk
    processed_chunks = []
    for chunk in chunks:
        # Apply LangChain processing here if needed
        processed_chunk = chunk  # Replace with actual processing
        processed_chunks.append(processed_chunk)
    
    # Combine processed chunks back into a single text
    processed_text = ",".join(processed_chunks)
    
    return processed_text

def concatenate_fields(document):
    # Define the list of fields you want to concatenate
    selected_field_names = [
        "issuerName",
        "issuerTicker",
        "Description",
        "pubDate",
        "txType",
        "tradeValue",
        "reportingGap",
        "filingDate",
        "txDate",
        "value",
        "gender",
        "firstName",
        "lastName",
        "party",
        "owner",
        "chamber",
        "price",
        "filingURL",
        "comment",
        # Add more fields as needed
    ]

    # Initialize an empty list to store processed field values
    processed_field_values = []

    # Iterate through the selected fields
    for field_name in selected_field_names:
        field_value = document.get(field_name, "")

        # Check if the field value is numeric (float or int)
        if isinstance(field_value, (int, float)):
            # Convert numeric value to string and add to the list
            processed_field_values.append(str(field_value))
        elif isinstance(field_value, str):
            # Add the string value to the list as is
            processed_field_values.append(field_value)
        else:
            # Handle other data types as needed
            processed_field_values.append(str(field_value))  # Convert to string

    # Join processed field values into a single text
    processed_text = " ".join(processed_field_values)

    return processed_text

def chunk_and_process_data(document):
    # Concatenate selected fields into a single text
    text = concatenate_fields(document)

    # Use LangChain to chunk and process the text
    processed_text = langchain_process(text)

    # Store processed data in the destination collection
    processed_document = {"text": processed_text}
    destination_collection.insert_one(processed_document)

def main():
    cursor = source_collection.find({})  # Retrieve all documents from the source collection

    for document in cursor:
        chunk_and_process_data(document)

if __name__ == "__main__":
    main()
