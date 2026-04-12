from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import os
import random
import requests
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


def average_category_score(category_scores) -> float | None:
    if not category_scores:
        return None

    scores = [cs.get("score") for cs in category_scores if cs and cs.get("score") is not None]
    if not scores:
        return None

    return sum(scores) / len(scores)

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

    return [
        {
            **senator,
            "score": average_category_score((s := get_senator_by_name(senator["name"])) and s.get("category_scores"))
        }
        for senator in senators
    ]


@app.get("/senators/{senator_name}")
def get_senator_controller(senator_name: str):
    senator_data = get_senator_by_name(name=senator_name)
    if senator_data is None:
        return {"message": f"Its somewhat fucked: {senator_name}"}

    seniority = int(senator_data['seniority'])
    state = senator_data['state']
    category_scores = get_senator_score(state, seniority) or []

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

    s = SenatorData(
        state=state,
        name=senator_data['name'],
        party=senator_data['party'],
        overall_score=sum([score.score for score in category_scores]) / len(
            category_scores) if category_scores else 0.0,
        category_scores=[ScoreData(category=score.category, score=score.score) for score in category_scores],
        headshot=headshot
    )

    return s

# "html=True" automatically serves index.html at the root of the mount path
app.mount("/", StaticFiles(directory="../client", html=True), name="static")
