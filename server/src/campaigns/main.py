from src.campaigns.lib import CampaignScraper
import csv

from src.campaigns.campaigns_llm import CampaignPromiseRetriever
from src.database.model import Senator, CategoryScore
from src.database.senator import create_senator

cs = CampaignScraper()
senators = []
analyzer = CampaignPromiseRetriever()

with open("data/119th_Congress_Senators_Campaigns.csv", mode='r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        if reader.line_num == 1:
            continue
        promise_list = cs.find_promise_list(row[3])
        print(row[0], row[1], promise_list)

        json_from_llm = analyzer.llm_analysis(promise_list)
        validated_json = analyzer.validate_senator_classification(json_from_llm)
        if validated_json is None:
            print("Validation failed, skipping...")
            continue

        data = validated_json.model_dump()
        categories = [
            CategoryScore(category=k, score=v["score"])
            for k, v in data["categories"].items()
            if v is not None and v["score"] != 0
        ]

        new_senator = Senator(
            state=row[0],
            name=row[1],
            party=row[2],
            campaign_website=row[3],
            promises=promise_list,
            category_scores=categories,
            seniority=int(row[4])
        )

        success = create_senator(new_senator)
