import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError, ConfigDict
from src.database.model import Senator, CategoryScore
from src.database.senator import create_senator

from src.analysis.llm_validation import ScoreEvidence

# Initialize the client

load_dotenv()

# Access variables
openrouter_key = os.getenv("OPENROUTER_API_KEY")
congress_key = os.getenv("CONGRESS_API_KEY")

class CampaignPromiseRetriever:
    def __init__(self):
        print("Initializing OpenAI client with key:", openrouter_key)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
        )

    def llm_analysis(self, campaign_promises):
        prompt = f"""
            You are scoring the campaign promises from the websites of a sitting U.S. senator. 
            
            Your task is to classify each campaign promise across a predefined set of policy categories and assign a score for each category.
            
            Scoring rules:
            -2 = strongly favors the first side listed in the category definition
            -1 = somewhat favors the first side
            0 = category is not meaningfully addressed, mixed, unclear, or neutral
            1 = somewhat favors the second side
            2 = strongly favors the second side
    
            Important rules:
            - Use only the campaign text provided.
            - You may only make highly likely, well-supported inferences from the text.
            - If a category is not clearly addressed, return 0.
            - Output valid JSON only.
            - Do not include markdown.
            - For each category, include both a score and a short evidence statement quoting or paraphrasing the campaign promise.
            - Do NOT include categories that are scored a 0
            - Every campaign promise should be given the same score when evaluated multiple times, ie. ensure consistent scoring across runs
    
            Return exactly this schema:
            {{
            "senator_name": "string",
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
            - foreign_aid_vs_isolationism: -2 = reduce foreign aid / isolationist, 2 = expand foreign aid / international engagement / interventionism
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

    def validate_senator_classification(self, data):
        try:
            validated = SenatorClassification.model_validate_json(data)
            print("Valid JSON")
            print(validated.model_dump())
            return validated

        except ValidationError as e:
            print(e)
            return None
            # TODO: Rerun LLM and hope it works on the second time (if it fails again give up)


class Categories(BaseModel):
    abortion: Optional[ScoreEvidence] = None
    affirmative_action: Optional[ScoreEvidence] = None
    balanced_budget_vs_expand_spending: Optional[ScoreEvidence] = None
    citizenship_pathways: Optional[ScoreEvidence] = None
    clean_energy_vs_fossil_fuels: Optional[ScoreEvidence] = None
    corporate_tax_rates: Optional[ScoreEvidence] = None
    crypto_gambling_corruption_regulation: Optional[ScoreEvidence] = None
    executive_power_limits: Optional[ScoreEvidence] = None
    foreign_aid_vs_isolationism: Optional[ScoreEvidence] = None
    free_trade_vs_isolationism: Optional[ScoreEvidence] = None
    gun_control: Optional[ScoreEvidence] = None
    immigration_border_wall_deportations: Optional[ScoreEvidence] = None
    israel_vs_palestine: Optional[ScoreEvidence] = None
    medicaid_cuts_vs_expansion: Optional[ScoreEvidence] = None
    minimum_wage: Optional[ScoreEvidence] = None
    obamacare_repeal_vs_expansion: Optional[ScoreEvidence] = None
    same_sex_marriage: Optional[ScoreEvidence] = None
    stock_trading_restrictions: Optional[ScoreEvidence] = None
    vaccines_public_health_vs_health_skepticism: Optional[ScoreEvidence] = None
    voter_id_and_election_restrictions: Optional[ScoreEvidence] = None

    model_config = ConfigDict(extra="forbid")


class SenatorClassification(BaseModel):
    senator_name: str
    categories: Categories

    model_config = ConfigDict(extra="forbid")

