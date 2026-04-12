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
            seniority=row[4]
        )

        success = create_senator(new_senator)
        break
#
# print("*****Dave McCormick's Promises******")
# cs.try_and_print_promises("https://www.davemccormickpa.com/day-one-promises/")
# #
# # print("*****Angela Alsobrooks's Promises*****")
# # cs.try_and_print_promises("https://www.angelaalsobrooks.com/priorities")
#
# print("*****Jim Bank's Promises******")
# cs.try_and_print_promises("https://banksforsenate.com/issues/")
#
# print("****Jim Justice's Promises*****")
# cs.try_and_print_promises("https://jimjusticewv.com/issues")
#
# print("****Lisa Blunt Rochester's Promises*****")
# cs.try_and_print_promises("https://lisabluntrochester.com/issues")
#
# print("*****John Curtis's Promises's*****")
# cs.try_and_print_promises("https://www.johncurtis.org/issues/")
#
# print("Gallego's Promises's*****")
# cs.try_and_print_promises("https://gallegoforarizona.com/issues/")
# ################
#
# print("Bernie Moreno's Promises")
# cs.try_and_print_promises("https://berniemoreno.com/about/")
#
# print("Tim Formt")
# cs.try_and_print_promises("https://timformt.com/meet-tim/")
#
# print("Elissa Slotkin")
# cs.try_and_print_promises("https://elissaslotkin.org/priorities/")
#
# print("Jon Husted")
# cs.try_and_print_promises("https://www.jonhustedforsenate.com/bio/")
#
# print("Ashley Moody")
# cs.try_and_print_promises("https://ashleymoody.com/priorities/")
#
# print("Adam Schiff")
# cs.try_and_print_promises("https://www.adamschiff.com/plans/")
#
# print("Andy Kim")
# cs.try_and_print_promises("https://www.andykim.com/issues/")
#
#
#
#
#
