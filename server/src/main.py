from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import random
import re
import requests
import json
from database.model import CategoryScore
from database.senator import get_senator, get_senator_score, get_senator_by_name

app = FastAPI()

# Let your frontend talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoreData(BaseModel):
    category: str
    score: float


class SenatorData(BaseModel):
    state: str  #
    name: str  #
    party: str  #
    overall_score: float
    category_scores: list[ScoreData]
    headshot: str

def convert_name(name: str) -> str:
    # Special cases:
    if name == "Britt, Katie Boyd":
        return "Katie Boyd Britt"
    elif name == "Luján, Ben Ray":
        return "Ben Lujan"

    result = re.search(r"(\b[A-Z][a-zA-Z\s]*\b), (\b[A-Z][a-zA-Z]*\b)", name)
    if result:
        return f"{result.group(2)} {result.group(1)}"
    return name

def overall_score(senate_score, bill_score):
    overall_score = 0
    for category_score in senate_score:
        for bill_category in bill_score:
            print(category_score)
            print(bill_category)
            if category_score.category == bill_category.category:
                overall_score += 4 - abs(category_score.score - bill_category.score)
    overall_score = overall_score/(4* len(senate_score))
    return overall_score

congress_key = os.getenv("CONGRESS_API_KEY")

@app.get("/states/{state}")
def get_senators(state: str):
    response = requests.get(
        f"https://api.congress.gov/v3/member/{state}?format=json&currentMember=true&api_key={congress_key}"
    )
    members = response.json()["members"]
    senators = [
        {**m, "name": convert_name(m.get("name"))}
        for m in members
        if "district" not in m
    ]

    return_list = []
    for senator in senators:
        s = get_senator_by_name(senator["name"])

        # Convert the raw lists of dicts into lists of CategoryScore objects
        senate_objs = [CategoryScore(**item) for item in s["category_scores"]]
        bill_objs = get_senator_score(s['state'], s["seniority"])

        # Pass the objects into the function
        oscore = overall_score(senate_objs, bill_objs)
        return_list.append({**senator, "score": oscore * 100})
    return return_list


@app.get("/senators/{senator_name}")
def get_senator_controller(senator_name: str):
    senator_data = get_senator_by_name(name=senator_name)
    if senator_data is None:
        return {"message": f"Its somewhat fucked: {senator_name}"}

    seniority = int(senator_data['seniority'])
    state = senator_data['state']
    bill_category_scores = get_senator_score(state, seniority) or []

    response = requests.get(
        f"https://api.congress.gov/v3/member/{state}?format=json&currentMember=true&api_key={congress_key}"
    )
    members = response.json()["members"]
    senators = [m for m in members if "district" not in m]
    headshot = next(
        (
            s.get("depiction", {}).get("imageUrl")
            for s in senators
            if convert_name(s.get("name", "")) == senator_name
        ),
        None,
    )

    o_score = overall_score(senator_data["category_scores"], bill_category_scores)
    s = SenatorData(
        state=state,
        name=senator_data['name'],
        party=senator_data['party'],
        overall_score= o_score*100,
        category_scores=[ScoreData(category=score.category, score=score.score) for score in bill_category_scores],
        headshot=headshot
    )

    return s




# "html=True" automatically serves index.html at the root of the mount path
app.mount("/", StaticFiles(directory="../../client", html=True), name="static")
