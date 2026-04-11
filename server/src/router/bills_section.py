from src.database.db_connection import get_collection
from server.src.database.model import Bill, Section

def create_bill(bill: Bill) -> int:
    bill_data = bill.model_dump(by_alias=True, exclude_none=True)
    bills_collection = get_collection("bills")
    try: 
        bills_collection.insert_one(bill_data)
    except Exception as e:
        print(f"Error occurred while inserting bill: {e}")
        return -1
    return 0

def create_section(section: Section) -> int:
    section_data = section.model_dump(by_alias=True, exclude_none=True)
    sections_collection = get_collection("sections")
    try: 
        sections_collection.insert_one(section_data)
    except Exception as e:
        print(f"Error occurred while inserting section: {e}")
        return -1
    return 0

def get_bill_score(bill_id: int) -> dict:
    sections_collection = get_collection("sections")
    try:
        sections = sections_collection.find({"bill_id": bill_id})
        category_scores = {}
        for section in sections:
            for category_score in section["category_scores"]:
                category = category_score["category"]
                score = category_score["score"]
                if category not in category_scores:
                    category_scores[category] = 0
                category_scores[category] += score
        return category_scores
    except Exception as e:
        print(f"Error occurred while retrieving bill score: {e}")
        return {}