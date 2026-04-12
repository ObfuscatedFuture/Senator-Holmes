from src.database.db_connection import get_collection
from src.database.model import Senator, CategoryScore
from src.database.vote import get_senator_vote

def create_senator(senator: Senator) -> int:
    senator_data = senator.model_dump(by_alias=True, exclude_none=True)
    senators_collection = get_collection("Senator")
    try: 
        senators_collection.insert_one(senator_data)
    except Exception as e:
        print(f"Error occurred while inserting senator: {e}")
        return -1
    return 0

def get_senator(state: str, seniority: int) -> Senator:
    senators_collection = get_collection("Senator")
    try:
        senator = senators_collection.find_one({"state": state, "seniority": seniority})
        if senator is None:
            print(f"No senator found with state: {state} and seniority: {seniority}")
            return None
        return senator
    except Exception as e:
        print(f"Error occurred while retrieving senator: {e}")
        return None

def get_senator(name: str) -> Senator:
    senators_collection = get_collection("Senator")
    try:
        senator = senators_collection.find_one({"name": name})
        if senator is None:
            print(f"No senator found with name: {name}")
            return None
        return senator
    except Exception as e:
        print(f"Error occurred while retrieving senator: {e}")
        return None

def get_senator_score(state: str, seniority: int) -> list[CategoryScore]:
    senators_collection = get_collection("Senator")
    try:
        senator = senators_collection.find_one({"state": state, "seniority": seniority})
        if senator is None:
            print(f"No senator found with state: {state} and seniority: {seniority}")
            return None
        return get_senator_vote(state, seniority)
    except Exception as e:
        print(f"Error occurred while retrieving score of senator: {e}")
        return None