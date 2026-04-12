from pydantic import BaseModel

class CategoryScore(BaseModel):
    category: str
    score: float

class Senator(BaseModel):
    state: str
    name: str
    seniority: int
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
    bill_title: str
    state: str
    seniority: int
    vote: int