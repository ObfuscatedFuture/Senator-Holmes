## This should do the full llm.py loop with all bills + the validation step
import llm_validation



# turns plaintext to json, then json to array 
        data = json.loads(completion.choices[0].message.content)
        categories = [
            [k, v["score"]] 
            for k, v in data["categories"].items() if v["score"] != 0
        ]
