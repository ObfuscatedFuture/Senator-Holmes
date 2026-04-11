from pydantic import BaseModel

class Promise(BaseModel):
    category: str
    description: str

class Senator(BaseModel):
    state: str
    seniority: int
    name: str
    party: str
    promises: list[Promise]

class Bill(BaseModel):
    bill_id: int
    short_title: str
    long_title: str

class CategoryScore(BaseModel):
    category: str
    score: int

class Section(BaseModel):
    bill_id: int
    section_id: int
    text: str
    category_scores: list[CategoryScore]

class Vote(BaseModel):
    bill_id: int
    state: str
    seniority: int
    vote: str