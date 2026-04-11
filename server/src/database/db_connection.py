from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import certifi

# Loading environement variables
load_dotenv()

print(os.getenv("MONGODB_URI"))
client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where(),server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)