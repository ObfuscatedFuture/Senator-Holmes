from fastapi import FastAPI
import requests
import os
import xml.etree.ElementTree as ET
from src.database.model import *
from src.database.bills import *

LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
LEGISCAN_BASE = "https://api.legiscan.com/"

# Step 1 - get bill details (contains roll_call_ids)
def get_bill(bill_id: int):
    response = requests.get(LEGISCAN_BASE, params={
        "key": LEGISCAN_API_KEY,
        "op": "getBill",
        "id": bill_id
    })
    return response.json()["bill"]

# Step 2 - get roll call votes for a specific vote on the bill
def get_roll_call(roll_call_id: int):
    response = requests.get(LEGISCAN_BASE, params={
        "key": LEGISCAN_API_KEY,
        "op": "getRollCall",
        "id": roll_call_id
    })
    print(response.json()["roll_call"])
    return response.json()["roll_call"]

# Step 3 - get person/senator details by people_id
def get_person(people_id: int):
    response = requests.get(LEGISCAN_BASE, params={
        "key": LEGISCAN_API_KEY,
        "op": "getPerson",
        "id": people_id
    })
    return response.json()["person"]

# All together - get every senator's vote for a bill
def get_votes_for_bill(bill_id: int):
    bill = get_bill(bill_id)
    
    results = []

    # bill has a list of votes, each with a roll_call_id
    for vote_summary in bill["votes"]:
        roll_call_id = vote_summary["roll_call_id"]
        roll_call = get_roll_call(roll_call_id)
        
        # roll_call has a list of individual votes
        for vote in roll_call["votes"]:
            people_id = vote["people_id"]
            vote_value = vote["vote_id"]  # 1=Yea, 2=Nay, 3=Not Voting, 4=Absent
            
            person = get_person(people_id)
            
            results.append({
                "name": person["name"],
                "party": person["party"],
                "state": person["state"],
                "vote": vote["vote_text"],  # "Yea", "Nay", "Not Voting", "Absent"
            })
    
    return results

bill = get_bill(42)

members = get_votes_for_bill(bill['bill_id'])
print(members)

