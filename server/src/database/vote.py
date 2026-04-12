from database.db_connection import get_collection
from database.model import Vote, CategoryScore
from database.bills import get_bill

def create_vote(vote: Vote) -> int:
    vote_data = vote.model_dump(by_alias=True, exclude_none=True)
    votes_collection = get_collection("Vote")
    try:
        if (get_senator_vote_on_bill(vote.state, vote.seniority, vote.bill_title) is not None):
            print(f"Vote with state: {vote.state}, seniority: {vote.seniority} and bill_title: {vote.bill_title} already exists.")
            return -1
        votes_collection.insert_one(vote_data)
    except Exception as e:
        print(f"Error occurred while inserting vote")
        return -1
    return 0

def get_senator_vote_on_bill(state: str, seniority: int, bill_title: str) -> Vote:
    votes_collection = get_collection("Vote")
    try:
        vote = votes_collection.find_one({"state": state, "seniority": seniority, "bill_title": bill_title})
        if vote is None:
            print(f"No vote found with state: {state}, seniority: {seniority} and bill_title: {bill_title}")
            return None
        return vote
    except Exception as e:
        print(f"Error occurred while retrieving vote: {e}")
        return None

def get_senator_vote(state: str, seniority: int) -> list[CategoryScore]:
    votes_collection = get_collection("Vote")
    try:
        votes = votes_collection.find({"state": state, "seniority": seniority})
        if votes is None:
            print(f"No votes found with state: {state} and seniority: {seniority}")
            return None
        
        category_totals: dict[str, dict[str, float]] = {}

        for vote in votes:
            vote_weight = vote.get("vote")
            bill = get_bill(vote.get("bill_title"))
            if bill is None:
                print(f"No bill found with bill_title: {vote.get('bill_title')}")
                continue

            for category_score in bill.get("category_scores"):
                category = category_score.get("category")
                score = category_score.get("score")
                if category is None or score is None:
                    continue

                if category not in category_totals:
                    category_totals[category] = {"weighted_sum": 0.0, "count": 0.0}

                category_totals[category]["weighted_sum"] += float(score) * float(vote_weight)
                category_totals[category]["count"] += 1.0
            
        average_scores: list[CategoryScore] = []
        for category, totals in category_totals.items():
            if totals["count"] == 0:
                continue
            average_score = totals["weighted_sum"] / totals["count"]
            average_scores.append(CategoryScore(category=category, score=average_score))
        
        return average_scores
         
    except Exception as e:
        print(f"Error occurred while retrieving vote of senator: {e}")
        return None