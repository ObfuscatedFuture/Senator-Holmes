## This should do the full llm.py loop with all bills + the validation step
import llm_validation
import llm

bill_text_sample = ""

# Initialize the BillAnalyzer
BillAnalyzer = llm.BillAnalyzer()


json_from_llm = BillAnalyzer.llm_analysis(bill_text_sample)

validated_json = llm_validation.BillClassification.model_validate_json(json_from_llm)


