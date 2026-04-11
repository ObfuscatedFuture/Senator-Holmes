from pydantic import BaseModel

class Senator(BaseModel):
    state: str
    seniority: int
    name: str
    party: str
    promises: list[str]

class CategoryScore(BaseModel):
    category: str
    score: int

class Bill(BaseModel):
    bill_id: int
    short_title: str
    long_title: str
    text: str
    category_scores: list[CategoryScore]

class Vote(BaseModel):
    bill_id: int
    state: str
    seniority: int
    vote: str