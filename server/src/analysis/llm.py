import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import json

# Initialize the client

load_dotenv()

# Access variables
openrouter_key = os.getenv("OPENROUTER_API_KEY")
congress_key = os.getenv("CONGRESS_API_KEY")


class BillAnalyzer:
    def __init__(self):
        print("Initializing OpenAI client with key:", openrouter_key)
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
        )

    def llm_analysis(self, bill_text):
        prompt = f"""
        You are analyzing the text of a political bill.

        Your task is to classify the bill across a predefined set of policy categories and assign a score for each category.

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
        - abortion: -2 = restricts abortion access, 2 = expands abortion access
        - gun_control: -2 = expands gun rights / reduces firearm regulation, 2 = increases gun regulation
        - voter_id_and_election_restrictions: -2 = expands ballot access / reduces restrictions, 2 = increases voter ID or election restrictions
        - free_trade_vs_isolationism: -2 = favors isolationism/protectionism, 2 = favors free trade/international economic openness
        - minimum_wage: -2 = opposes or lowers minimum wage mandates, 2 = raises or expands minimum wage protections
        - balanced_budget_vs_expand_spending: -2 = expands government spending/deficits, 2 = cuts spending / prioritizes budget restraint
        - obamacare_repeal_vs_expansion: -2 = repeals or weakens ACA/Obamacare, 2 = expands ACA-style coverage
        - medicaid_cuts_vs_expansion: -2 = cuts Medicaid, 2 = expands Medicaid
        - vaccines_public_health_vs_health_skepticism: -2 = supports vaccine skepticism / reduces mandates, 2 = supports public health mandates and vaccine programs
        - immigration_border_wall_deportations: -2 = expands immigration access / reduces enforcement, 2 = increases wall, deportations, detention, or border enforcement
        - citizenship_pathways: -2 = restricts pathways to citizenship, 2 = expands pathways to citizenship
        - foreign_aid_vs_isolationism: -2 = reduces foreign aid / isolationist, 2 = expands foreign aid / international engagement
        - israel_vs_palestine: -2 = more pro-Palestinian position, 2 = more pro-Israel position
        - same_sex_marriage: -2 = restricts same-sex marriage rights, 2 = protects or expands same-sex marriage rights
        - affirmative_action: -2 = restricts affirmative action, 2 = supports or expands affirmative action
        - clean_energy_vs_fossil_fuels: -2 = favors fossil fuels / weakens climate policy, 2 = favors clean energy / strengthens climate policy
        - executive_power_limits: -2 = expands executive discretion/power, 2 = limits executive power / increases oversight
        - crypto_gambling_corruption_regulation: -2 = reduces regulation or restrictions, 2 = increases regulation / anti-corruption restrictions
        - corporate_tax_rates: -2 = lowers corporate taxes, 2 = raises corporate taxes
        - stock_trading_restrictions: -2 = opposes restrictions on officeholders trading, 2 = imposes stronger trading bans or disclosure rules


        Here is the bill text:
        {bill_text}
        """

        # Make a request
        completion = self.client.chat.completions.create(
            model="google/gemini-2.5-flash-lite",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Please comment this code idk what it does
        data = json.loads(completion.choices[0].message.content)
        categories = [
            [k, v["score"]] 
            for k, v in data["categories"].items() if v["score"] != 0
        ]

        print(categories)
        return completion.choices[0].message.content

