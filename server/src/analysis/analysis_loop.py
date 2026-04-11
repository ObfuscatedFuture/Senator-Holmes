## This should do the full llm.py loop with all bills + the validation step
import llm_validation
import llm
import json

f = open('test_bill.txt')
bill_text_sample = f.read()
# Initialize the BillAnalyzer


BillAnalyzer = llm.BillAnalyzer()

json_from_llm = BillAnalyzer.llm_analysis(bill_text_sample)

validated_json = llm_validation.BillClassification.model_validate_json(json_from_llm)




# turns plaintext to json, then json to array 
data = json.loads(validated_json)
categories = [
    [k, v["score"]] 
    for k, v in data["categories"].items() if v["score"] != 0
        ]
