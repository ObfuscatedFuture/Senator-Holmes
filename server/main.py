from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import os
import random
import requests
from src.database.senator import get_senator, get_senator_score, get_senator_by_name

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

class StateData(BaseModel):
    state: str
    senators: list[SenatorData]




congress_key = os.getenv("CONGRESS_API_KEY")

@app.get("/states/{state}")
def get_senators(state: str):
    response = requests.get(
        f"https://api.congress.gov/v3/member/{state}?format=json&currentMember=true&api_key={congress_key}"
    )
    members = response.json()["members"]
    senators = [m for m in members if "district" not in m]

    return [
        {
            **senator,
            "score": (
                sum(cs.score for cs in s.category_scores) / len(s.category_scores)
                if (s := get_senator_by_name(senator["name"])) and s.category_scores
                else None
            )
        }
        for senator in senators
    ]

# TODO: Add the endpoint with more info (like per category scores)
@app.get("/senators/{senator_name}")
def get_senator_controller(senator_name: str):
    senator_data = get_senator_by_name(name=senator_name)
    if senator_data is None:
        return {"message": f"Its somewhat fucked: {senator_name}"}

    seniority = int(senator_data['seniority'])
    state = senator_data['state']
    category_scores = get_senator_score(state, seniority)
    if category_scores is None:
        return {"message": f"Its mega fucked: {senator_name}"}

    s = SenatorData(
        state=state,
        name=senator_data['name'],
        party=senator_data['party'],
        overall_score=sum([score.score for score in category_scores]) / len(
            category_scores) if category_scores else 0.0,
        category_scores=[ScoreData(category=score.category, score=score.score) for score in category_scores]
    )

    return s

# "html=True" automatically serves index.html at the root of the mount path
app.mount("/", StaticFiles(directory="../client", html=True), name="static")
