## This should do the full llm.py loop with all bills + the validation step
import llm_validation
import llm
import json
import json

f = open('test_bill.txt')
bill_text_sample = f.read()

# Initialize the BillAnalyzer
BillAnalyzer = llm.BillAnalyzer()

json_from_llm = BillAnalyzer.llm_analysis(bill_text_sample)
validated_json = llm_validation.validate_bill_classification(json_from_llm)

if validated_json is None:
    print("Validation failed must retry")

print(validated_json)