import requests
import os
from dotenv import load_dotenv

base_url = 'https://api.congress.gov/v3'
timeout = 1
session = requests.Session()

load_dotenv()

congress_key = os.getenv("CONGRESS_API_KEY")
print(congress_key)

url_endpoint = '/bill?format=json&api_key=' + os.getenv("CONGRESS_API_KEY")

print(session.get(base_url + url_endpoint, timeout=timeout).content)

