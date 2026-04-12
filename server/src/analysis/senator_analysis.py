from fastapi import FastAPI
import requests
import os
import xml.etree.ElementTree as ET
from src.database.model import *
from src.database.bills import *
from dotenv import load_dotenv

import requests
import xml.etree.ElementTree as ET

load_dotenv()

LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
LEGISCAN_BASE = "https://api.legiscan.com/"
import requests
import os
from dotenv import load_dotenv

load_dotenv()

LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
LEGISCAN_BASE = "https://api.legiscan.com/"

def search_bill(bill_number: str, state: str = "US"):
    """Search for a bill by number and return the legiscan bill_id"""
    response = requests.get(LEGISCAN_BASE, params={
        "key": LEGISCAN_API_KEY,
        "op": "getSearch",
        "query": bill_number,
        "state": state
    })
    data = response.json()

    results = data.get("searchresult", {})
    bills = [v for k, v in results.items() if k != "summary"]

    if not bills:
        print(f"No bills found for {bill_number}")
        return None

    # find exact match on bill number
    for bill in bills:
        if bill.get("bill_number") == bill_number:
            return bill["bill_id"]

    # fallback to first result
    return bills[0]["bill_id"]


def get_bill(bill_id: int):
    """Get full bill details including votes"""
    response = requests.get(LEGISCAN_BASE, params={
        "key": LEGISCAN_API_KEY,
        "op": "getBill",
        "id": bill_id
    })
    data = response.json()

    if data.get("status") == "ERROR":
        print(f"Error: {data.get('alert')}")
        return None

    return data["bill"]

def get_roll_call(roll_call_id: int):
    response = requests.get(LEGISCAN_BASE, params={
        "key": LEGISCAN_API_KEY,
        "op": "getRollCall",
        "id": roll_call_id
    })
    data = response.json()
    if data.get("status") == "ERROR":
        print(f"Error: {data.get('alert')}")
        return None
    return data["roll_call"]

# cache to avoid repeat API calls for same person
person_cache = {}

def get_person(people_id: int):
    if people_id in person_cache:
        return person_cache[people_id]
    
    response = requests.get(LEGISCAN_BASE, params={
        "key": LEGISCAN_API_KEY,
        "op": "getPerson",
        "id": people_id
    })
    data = response.json()

    if data.get("status") == "ERROR":
        print(f"Error: {data.get('alert')}")
        return None

    person = data["person"]
    person_cache[people_id] = person  # cache it
    return person

def get_rep_votes_for_bill(bill_number: str, state: str = "US"):
    bill_id = search_bill(bill_number, state)
    if not bill_id:
        return None

    bill = get_bill(bill_id)
    if not bill or not bill.get("votes"):
        print(f"No votes found for {bill_number}")
        return None

    senate_votes = []
    for vote_summary in bill["votes"]:
        roll_call_id = vote_summary["roll_call_id"]
        roll_call = get_roll_call(roll_call_id)
        if not roll_call:
            continue

        chamber = roll_call.get("chamber")
        if chamber != "H":
            continue

        senators = []
        for vote in roll_call.get("votes", []):
            people_id = vote.get("people_id")
            person = get_person(people_id)
            if not person:
                continue
            senators.append({
                "name": person["name"],
                "party": person["party"],
                "vote": vote["vote_text"]
            })

        senate_votes.append({
            "roll_call_id": roll_call_id,
            "description": vote_summary.get("desc"),
            "date": vote_summary.get("date"),
            "yea": vote_summary.get("yea"),
            "nay": vote_summary.get("nay"),
            "senators": senators
        })

    if not senate_votes:
        print(f"No senate votes found for {bill_number}")
        return None

    # return only the most recent senate vote
    most_recent = sorted(senate_votes, key=lambda v: v["date"], reverse=True)[0]
    return most_recent



# usage
result = get_rep_votes_for_bill("District of Columbia Appropriations Act, 2026 Judiciary Appropriations Act, 2026 Executive Office of the President Appropriations Act, 2026 Department of the Treasury Appropriations Act, 2026 Transportation, Housing and Urban Development, and Related Agencies Appropriations Act, 2026 Department of Transportation Appropriations Act, 2026 Department of Defense Appropriations Act, 2026 Further Continuing Appropriations Act, 2026 Financial Services and General Government Appropriations Act, 2026 Department of Health and Human Services Appropriations Act, 2026 Department of Education Appropriations Act, 2026 Department of Housing and Urban Development Appropriations Act, 2026 National Security, Department of State, and Related Programs Appropriations Act, 2026 Department of Labor Appropriations Act, 2026 Departments of Labor, Health and Human Services, and Education, and Related Agencies Appropriations Act, 2026", state="US")

if result:
    print(f"\n{result['description']} ({result['date']})")
    print(f"Yea: {result['yea']} | Nay: {result['nay']}")
    for senator in result["senators"]:
        print(f"  {senator['name']}: {senator['vote']}")