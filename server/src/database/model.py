from pydantic import BaseModel

class CategoryScore(BaseModel):
    category: str
    score: float

class Senator(BaseModel):
    state: str
    name: str
    party: str
    campaign_website: str
    promises: list[str]
    category_scores: list[CategoryScore]

class Bill(BaseModel):
    bill_id: int
    title: str
    text: str
    category_scores: list[CategoryScore]

class Vote(BaseModel):
    bill_id: int
    state: str
    seniority: int
    vote: int