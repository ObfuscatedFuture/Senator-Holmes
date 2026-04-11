from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Let your frontend talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    text: str

@app.get("/state/{state}")
def get_senators(state: str):
    return {"state": state, "message": "Here are the senators for this state"}

@app.get("/senators/{senator_name}")
def get_senator(senator_name: str):
    return {"senator_name": senator_name, "message": "Here is the information for this senator"}


@app.post("/analyze")
def analyze(data: InputData):
    return {
        "original_text": data.text,
        "length": len(data.text),
        "uppercase": data.text.upper()
    }