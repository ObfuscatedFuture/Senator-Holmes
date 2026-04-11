from fastapi import FastAPI
import requests
import os
import xml.etree.ElementTree as ET
from database.model import *
from database.bills import *
CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")
BASE_URL = "https://api.congress.gov/v3"

def get_senator_votes_from_bill(congress: int, bill_type: str, bill_number: int):
    # step 1 - get the vote URL from bill actions
    response = requests.get(
        f"{BASE_URL}/bill/{congress}/{bill_type.lower()}/{bill_number}/actions",
        params={"api_key": CONGRESS_API_KEY, "format": "json"}
    )
    actions = response.json()["actions"]
    
    vote_url = None
    for action in actions:
        if "recordedVotes" in action:
            for vote in action["recordedVotes"]:
                if vote["chamber"] == "Senate":
                    vote_url = vote["url"]
                    break

    if not vote_url:
        return None

    # step 2 - follow the URL to get individual senator votes
    response = requests.get(vote_url)
    root = ET.fromstring(response.text)

    members = []
    for member in root.findall(".//member"):
        members.append({
            "name": member.findtext("last_name") + ", " + member.findtext("first_name"),
            "party": member.findtext("party"),
            "state": member.findtext("state"),
            "vote_cast": member.findtext("vote_cast")
        })
    
    return members

bill = get_bill(370)

