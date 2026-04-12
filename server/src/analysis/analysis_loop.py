from fastapi import FastAPI
import requests
import os
from src.database.bills import create_bill
from src.database.model import Bill, CategoryScore
from src.analysis.llm_validation import validate_bill_classification
from src.analysis.llm import BillAnalyzer
from src.analysis.senator_analysis import get_votes_for_bill, search_bill, get_bill

app = FastAPI()

CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")
BASE_URL = "https://api.congress.gov/v3"

def get_bill_text_versions(congress: int, bill_type: str, bill_number: int):
    response = requests.get(
        f"{BASE_URL}/bill/{congress}/{bill_type.lower()}/{bill_number}/text",
        params={"api_key": CONGRESS_API_KEY, "format": "json"}
    )
    return response.json()

def get_bill_text_clean(congress: int, bill_type: str, bill_number: int):
    versions = get_bill_text_versions(congress, bill_type, bill_number)
    if "textVersions" not in versions or len(versions["textVersions"]) == 0:
        return None
    latest = versions["textVersions"][0]
    htm_url = next((f["url"] for f in latest["formats"] if f["type"] == "Formatted Text"), None)
    if not htm_url:
        return None
    response = requests.get(htm_url)
    return response.text

def get_congress_bills(congress: int = 119, limit: int = 500, offset: int = 500):
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

BA = BillAnalyzer()

response = get_congress_bills()
bills = response['bills']

for bill in bills:
    bill_number = bill['number']
    bill_type = bill['type']
    bill_title = bill['title']

    print(f"\nProcessing: {bill_type}{bill_number} - {bill_title}")

    # step 1 - check if bill has senate voting data in legiscan
    # format bill number for legiscan e.g. "S1", "HR42"
    legiscan_bill_number = f"{bill_type}{bill_number}"
    
    senate_vote = get_votes_for_bill(legiscan_bill_number, chamber="S", state="US")
    
    if not senate_vote:
        print(f"No senate vote found for {legiscan_bill_number}, skipping...")
        continue

    print(f"Senate vote found: {senate_vote['description']} ({senate_vote['date']})")

    # step 2 - get bill text
    bill_text = get_bill_text_clean(congress=119, bill_type=bill_type, bill_number=bill_number)
    if not bill_text:
        print(f"No text found for {legiscan_bill_number}, skipping...")
        continue

    # step 3 - run LLM analysis
    json_from_llm = BA.llm_analysis(bill_text)
    validated_json = validate_bill_classification(json_from_llm)

    if validated_json is None:
        print("Validation failed, skipping...")
        continue

    # step 4 - save to database
    data = validated_json.model_dump()
    categories = [
        CategoryScore(category=k, score=v["score"])
        for k, v in data["categories"].items()
        if v is not None and v["score"] != 0
    ]

    new_bill = Bill(
        bill_id=bill_number,
        title=bill_title,
        text=bill_text,
        category_scores=categories
    )

    create_bill(new_bill)
    print(f"Saved {legiscan_bill_number} to database with {len(categories)} categories")