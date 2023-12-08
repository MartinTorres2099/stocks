# This code imports a CSV file into a mondodb table.
# Make sure the mondodb application is running.
import pandas as pd
import pymongo

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["stocks_db"]
collection = db["stocks_collection"]

def main():
    # Load data from CSV file
    csv_file_path = "C:/git/stocks/data/stocktrade.csv"
    data = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a list of dictionaries for MongoDB insertion
    data_dict_list = data.to_dict(orient='records')

    # Insert data into MongoDB collection
    collection.insert_many(data_dict_list)

if __name__ == "__main__":
    main()
