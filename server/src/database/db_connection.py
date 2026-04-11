from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import certifi

# Loading environement variables
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where(),server_api=ServerApi('1'))
database = client["BitcampDemo"]

def get_collection(collection_name):
    return database[collection_name]