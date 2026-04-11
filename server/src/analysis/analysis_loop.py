## This should do the full llm.py loop with all bills + the validation step

from fastapi import FastAPI
import requests
import os

from src.database.bills import create_bill
from src.database.model import Bill, CategoryScore
from src.analysis.llm_validation import validate_bill_classification
from src.analysis.llm import BillAnalyzer

app = FastAPI()

CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")
BASE_URL = "https://api.congress.gov/v3"

# get bills for a specific congress
@app.get("/bills")
def get_bills(congress: int = 119, limit: int = 1, offset: int = 500):
    response = requests.get(
        f"{BASE_URL}/bill/{congress}",
        params={
            "api_key": CONGRESS_API_KEY,
            "limit": limit,
            "offset": offset,
            "format": "json"
        }
    )
    return response.json()

#get the text versions a bill
def get_bill_text_versions(congress: int, bill_type: str, bill_number: int):
    response = requests.get(
        f"{BASE_URL}/bill/{congress}/{bill_type.lower()}/{bill_number}/text",  # .lower() here
        params={"api_key": CONGRESS_API_KEY, "format": "json"}
    )
    return response.json()

#return the actual text of a bill
def get_bill_text_clean(congress: int, bill_type: str, bill_number: int):
    versions = get_bill_text_versions(congress, bill_type, bill_number)
    
    # guard against missing text
    if "textVersions" not in versions or len(versions["textVersions"]) == 0:
        return None  # or return "" 
    
    latest = versions["textVersions"][0]
    htm_url = next((f["url"] for f in latest["formats"] if f["type"] == "Formatted Text"), None)
    
    if not htm_url:
        return None
    
    response = requests.get(htm_url)
    return response.text


response = get_bills()
bills =  response['bills']
BA = BillAnalyzer()

for bill in bills:
    bill_id = bill['number']
    bill_type = bill['type']
    bill_text = get_bill_text_clean(congress= 119, bill_type= bill_type, bill_number=bill_id)
    json_from_llm = BA.llm_analysis(bill_text)
    validated_json = validate_bill_classification(json_from_llm)
    if validated_json is None:
        print("Validation failed must retry")
    else:
        data = validated_json.model_dump()

        categories = [
            new_category := CategoryScore(category=k, score=v["score"]) for k, v in data["categories"].items() if v is not None and v["score"] != 0
        ]
        print("\n categories", categories)
        new_bill = Bill(
            bill_id=bill_id,
            title=bill['title'],
            text=bill_text,
            category_scores=categories
        )
        create_bill(new_bill)
