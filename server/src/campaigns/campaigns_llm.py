import csv
from collections import defaultdict

from pydantic import BaseModel, HttpUrl
from typing import List

import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import json

from typing import Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict
from src.database.model import Senator, CategoryScore
from src.database.senator import create_senator

# Initialize the client

load_dotenv()

# Access variables
openrouter_key = os.getenv("OPENROUTER_API_KEY")
congress_key = os.getenv("CONGRESS_API_KEY")

# class CategoryScore(BaseModel):
#     category: str
#     score: float

# class Senator(BaseModel):
#     state: str
#     name: str
#     party: str
#     campaign_website: str
#     promises: list[str]
#     category_scores: list[CategoryScore]


class CampaignPromiseRetriever:
    def __init__(self):
        print("Initializing OpenAI client with key:", openrouter_key)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
        )

    def llm_analysis(self, campaign_promises):
        prompt = f"""
            You are scoring the campaign promise websites of sitting U.S. senators in their first terms. 
            Provide a JSON 
            
            Scoring rules:
            -2 = strongly favors the first side listed in the category definition
            -1 = somewhat favors the first side
            0 = category is not meaningfully addressed, mixed, unclear, or neutral
            1 = somewhat favors the second side
            2 = strongly favors the second side
    
            Important rules:
            - Use only the bill text provided.
            - Do not infer positions not supported by the text.
            - If a category is not clearly addressed, return 0.
            - Output valid JSON only.
            - Do not include markdown.
            - For each category, include both a score and a short evidence statement quoting or paraphrasing the bill.
            - Do NOT include categories that are scored a 0
            - Every bill should be given the same score when evaluated multiple times, ie. ensure consistent scoring across runs
    
            Return exactly this schema:
            {{
            "bill_title": "string",
            "categories": {{
                "abortion": {{
                "score": 0
                }},
                "affirmative_action": {{
                "score": 0
                }},
                "balanced_budget_vs_expand_spending": {{
                "score": 0
                }},
                "citizenship_pathways": {{
                "score": 0
                }},
                "clean_energy_vs_fossil_fuels": {{
                "score": 0
                }},
                "corporate_tax_rates": {{
                "score": 0
                }},
                "crypto_gambling_corruption_regulation": {{
                "score": 0
                }},
                "executive_power_limits": {{
                "score": 0
                }},
                "foreign_aid_vs_isolationism": {{
                "score": 0
                }},
                "free_trade_vs_isolationism": {{
                "score": 0
                }},
                "gun_control": {{
                "score": 0
                }},
                "immigration_border_wall_deportations": {{
                "score": 0
                }},
                "israel_vs_palestine": {{
                "score": 0
                }},
                "medicaid_cuts_vs_expansion": {{
                "score": 0
                }},
                "minimum_wage": {{
                "score": 0
                }},
                "obamacare_repeal_vs_expansion": {{
                "score": 0
                }},
                "same_sex_marriage": {{
                "score": 0
                }},
                "stock_trading_restrictions": {{
                "score": 0
                }},
                "vaccines_public_health_vs_health_skepticism": {{
                "score": 0
                }},
                "voter_id_and_election_restrictions": {{
                "score": 0
                }}
            }}
            }}
    
    
            Category definitions:
            - abortion: -2 = restrict abortion access, 2 = expand abortion access
            - gun_control: -2 = expand gun rights / reduce firearm regulation, 2 = increase gun regulation
            - voter_id_and_election_restrictions: -2 = expand ballot access / reduce restrictions, 2 = increase voter ID or election restrictions
            - free_trade_vs_isolationism: -2 = favor isolationism/protectionism, 2 = favor free trade/international economic openness
            - minimum_wage: -2 = oppose or lower minimum wage mandates, 2 = raise or expand minimum wage protections
            - balanced_budget_vs_expand_spending: -2 = expand government spending/deficits, 2 = cut spending / prioritize budget restraint
            - obamacare_repeal_vs_expansion: -2 = repeal or weaken ACA/Obamacare, 2 = expand ACA-style coverage
            - medicaid_cuts_vs_expansion: -2 = cut Medicaid, 2 = expand Medicaid
            - vaccines_public_health_vs_health_skepticism: -2 = support vaccine skepticism / reduce mandates, 2 = support public health mandates and vaccine programs
            - immigration_border_wall_deportations: -2 = expand immigration access / reduce enforcement, 2 = increase wall, deportation, detention, or border enforcement
            - citizenship_pathways: -2 = restrict pathways to citizenship, 2 = expand pathways to citizenship
            - foreign_aid_vs_isolationism: -2 = reduce foreign aid / isolationist, 2 = expand foreign aid / international engagement
            - israel_vs_palestine: -2 = more pro-Palestinian position, 2 = more pro-Israel position
            - same_sex_marriage: -2 = restrict same-sex marriage rights, 2 = protect or expand same-sex marriage rights
            - affirmative_action: -2 = restrict affirmative action, 2 = support or expand affirmative action
            - clean_energy_vs_fossil_fuels: -2 = favor fossil fuels / weaken climate policy, 2 = favor clean energy / strengthen climate policy
            - executive_power_limits: -2 = expand executive discretion/power, 2 = limit executive power / increase oversight
            - crypto_gambling_corruption_regulation: -2 = reduce regulation or restrictions, 2 = increase regulation / anti-corruption restrictions
            - corporate_tax_rates: -2 = lower corporate taxes, 2 = raise corporate taxes
            - stock_trading_restrictions: -2 = oppose restrictions on officeholders trading, 2 = imposes stronger trading bans or disclosure rules
    
    
            Here are their campaign promises:
            {campaign_promises}
            """


        # Make a request
        completion = self.client.chat.completions.create(
            model="google/gemini-2.5-flash-lite",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content

CPR = CampaignPromiseRetriever()
#TODO
CPR.llm_analysis("Call from scraper")

class CategoryScore(BaseModel):
    score: int = Field(..., ge=-2, le=2)
    evidence: Optional[str] = None


class Categories(BaseModel):
    abortion: Optional[CategoryScore] = None
    affirmative_action: Optional[CategoryScore] = None
    balanced_budget_vs_expand_spending: Optional[CategoryScore] = None
    citizenship_pathways: Optional[CategoryScore] = None
    clean_energy_vs_fossil_fuels: Optional[CategoryScore] = None
    corporate_tax_rates: Optional[CategoryScore] = None
    crypto_gambling_corruption_regulation: Optional[CategoryScore] = None
    executive_power_limits: Optional[CategoryScore] = None
    foreign_aid_vs_isolationism: Optional[CategoryScore] = None
    free_trade_vs_isolationism: Optional[CategoryScore] = None
    gun_control: Optional[CategoryScore] = None
    immigration_border_wall_deportations: Optional[CategoryScore] = None
    israel_vs_palestine: Optional[CategoryScore] = None
    medicaid_cuts_vs_expansion: Optional[CategoryScore] = None
    minimum_wage: Optional[CategoryScore] = None
    obamacare_repeal_vs_expansion: Optional[CategoryScore] = None
    same_sex_marriage: Optional[CategoryScore] = None
    stock_trading_restrictions: Optional[CategoryScore] = None
    vaccines_public_health_vs_health_skepticism: Optional[CategoryScore] = None
    voter_id_and_election_restrictions: Optional[CategoryScore] = None

    model_config = ConfigDict(extra="forbid")

# class CategoryScore(BaseModel):
#     category: str
#     score: float

# class Senator(BaseModel):
#     state: str
#     name: str
#     party: str
#     campaign_website: str
#     promises: list[str]
#     category_scores: list[CategoryScore]

class SenatorClassification(BaseModel):
    senator_name: str
    categories: Categories

    model_config = ConfigDict(extra="forbid")

def validate_senator_classification(data):
    try:
        validated = SenatorClassification.model_validate_json(data)
        print("Valid JSON")
        print(validated.model_dump())
        return validated
        
    except ValidationError as e:
        print(e)
        return None
        #TODO: Rerun LLM and hope it works on the second time (if it fails again give up)


BA = CampaignPromiseRetriever()
campaign_promises = "TODO ADD CAMPAIGN PROMISES"

json_from_llm = BA.llm_analysis(campaign_promises)
validated_json = validate_senator_classification(json_from_llm)

if validated_json is None:
    #print("Validation failed, skipping...")
    #TODO: This should break so probably invert this if statement
    pass

# step 4 - save to database
data = validated_json.model_dump()
categories = [
    CategoryScore(category=k, score=v["score"])
    for k, v in data["categories"].items()
    if v is not None and v["score"] != 0
]

new_senator = Senator(
    state="TODO",
    name=data["senator_name"],
    party="TODO",
    campaign_website="TODO",
    promises=campaign_promises,
    category_scores=categories
    
)

create_senator(new_senator)

states_dict = defaultdict(list)

with open("server/src/campaigns/119th_Congress_Senators_Campaigns.csv", newline="") as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        states_dict[row["State"]].append(
            Senator(
                state=row["State"],
                name=row["Name"],
                party=row["Party"],
                campaign_website=row["Campaign Website"],
                promises=#TODO ADD PROMISES
                category_scores=#TODO ADD CATEGORY SCORES
            )
        )


