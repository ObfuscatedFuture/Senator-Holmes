from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.database.senator import get_senator, get_senator_score


app = FastAPI()

# Let your frontend talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class scoreData(BaseModel):
    category: str
    score: float
class SenatorData(BaseModel):
    state: str #
    name: str #
    party: str #
    overall_score: float
    category_scores: list[scoreData]


#TODO: Add the endpoint with more info (like per category scores)
@app.get("/senators/{senator_name}")
def get_senator(senator_name: str):
    senator_data = get_senator(name=senator_name)
    if senator_data is None:
        return {"message": f"Its fucked: {senator_name}"}
    
    seniority = int(senator_data['seniority'])
    state = senator_data['state']
    category_scores = get_senator_score(state, seniority)
    if category_scores is None:
        return {"message": f"Its fucked: {senator_name}"}
    
    s = SenatorData(
        state=state,
        name=senator_data['name'],
        party=senator_data['party'],
        overall_score=sum([score.score for score in category_scores]) / len(category_scores) if category_scores else 0.0,
        category_scores=[scoreData(category=score.category, score=score.score) for score in category_scores]
    )

    return s