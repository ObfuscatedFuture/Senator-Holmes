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

class Section(BaseModel):
    bill_id: int
    section_id: int
    text: str
    category: str
    score: int

class Vote(BaseModel):
    bill_id: int
    state: str
    seniority: int
    vote: str