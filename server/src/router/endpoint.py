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

class SenatorData(BaseModel):
    state: str
    name: str
    party: str
    image_url: str
    trust_score: float
class StateData(BaseModel):
    state: str
    senators: list[SenatorData]


@app.get("/state/{state}")
def get_senators(state: str):

    # { Example Response: 
    #   "state": "Maryland",
    #   "senators": [
    #     {
    #       "name": "Chris Van Hollen",
    #       "party": "Democrat",
    #       "image_url": "...",
    #       "trust_score": 0.85
    #     },
    #     {
    #        "name": "Ben Van Hollen",
    #       "party": "Democrat",
    #       "image_url": "...",
    #       "trust_score": 0.69
    #     }
    #   ]
    # }

    StateData(
        state=state,
        senators=[
            SenatorData(
                name="Chris Van Hollen",
                party="Democrat",
                image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Chris_Van_Hollen%2C_official_portrait%2C_116th_Congress.jpg/330px-Chris_Van_Hollen%2C_official_portrait%2C_116th_Congress.jpg",
                trust_score=0.85
            ),
            SenatorData(
                name="Ben Van Hollen",
                party="Democrat",
                image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Chris_Van_Hollen%2C_official_portrait%2C_116th_Congress.jpg/330px-Chris_Van_Hollen%2C_official_portrait%2C_116th_Congress.jpg",
                trust_score=0.69
            )
        ]
    )
    
    return {"state": state, "message": "Here are the senators for this state"}

#TODO: Add the endpoint with more info (like per category scores)
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