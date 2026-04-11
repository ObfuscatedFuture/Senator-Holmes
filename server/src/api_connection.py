import requests
from typing import Optional, Dict, Any
import os

base_url = 'https://api.congress.gov/v3'
timeout = 0.1
session = requests.Session()


url_endpoint = '/bill?format=json&api_key=' + os.getenv("CONGRESS_API_KEY")

print(session.get(base_url + url_endpoint, timeout=timeout))

