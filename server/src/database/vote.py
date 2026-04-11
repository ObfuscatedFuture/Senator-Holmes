from src.database.db_connection import get_collection
from src.database.model import Vote, CategoryScore
from src.database.bills import get_bill

def create_vote(vote: Vote) -> int:
    vote_data = vote.model_dump(by_alias=True, exclude_none=True)
    votes_collection = get_collection("Vote")
    try: 
        votes_collection.insert_one(vote_data)
    except Exception as e:
        print(f"Error occurred while inserting vote")
        return -1
    return 0

def get_senator_vote(state: str, seniority: int) -> list[CategoryScore]:
    votes_collection = get_collection("Vote")
    try:
        votes = votes_collection.find({"state": state, "seniority": seniority})
        if votes is None:
            print(f"No votes found with state: {state} and seniority: {seniority}")
            return None
        # Doesn't work right now
        for vote in votes:
            vote_weight = vote.get("vote")
            bill = get_bill(vote.get("bill_id"))
            if bill is None:
                print(f"No bill found with bill_id: {vote.get('bill_id')}")
                continue
         
    except Exception as e:
        print(f"Error occurred while retrieving vote of senator: {e}")
        return None