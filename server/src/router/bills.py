from src.database.db_connection import get_collection
from src.database.model import Bill

def create_bill(bill: Bill) -> int:
    bill_data = bill.model_dump(by_alias=True, exclude_none=True)
    bills_collection = get_collection("Bill")
    if (get_bill(bill.bill_id) is not None):
        print(f"Bill with ID {bill.bill_id} already exists.")
        return -1
    try: 
        bills_collection.insert_one(bill_data)
    except Exception as e:
        print(f"Error occurred while inserting bill: {e}")
        return -1
    return 0

def get_bill(bill_id: int) -> Bill:
    bill_collection = get_collection("Bill")
    try:
        bill = bill_collection.find_one({"bill_id": bill_id})
        if bill is None:
            print(f"No bill found with bill_id: {bill_id}")
            return None
        return bill
    except Exception as e:
        print(f"Error occurred while retrieving bill: {e}")
        return None