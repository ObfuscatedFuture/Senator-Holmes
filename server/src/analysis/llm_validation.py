from typing import Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict


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


class BillClassification(BaseModel):
    bill_title: str
    categories: Categories

    model_config = ConfigDict(extra="forbid")


# Example usage
data = {
    "bill_title": "Safeguard American Voter Eligibility Act or the SAVE Act",
    "categories": {
        "abortion": {"score": 0},
        "affirmative_action": {"score": 0},
        "balanced_budget_vs_expand_spending": {"score": 0},
        "citizenship_pathways": {"score": 0},
        "clean_energy_vs_fossil_fuels": {"score": 0},
        "corporate_tax_rates": {"score": 0},
        "crypto_gambling_corruption_regulation": {"score": 0},
        "executive_power_limits": {"score": 0},
        "foreign_aid_vs_isolationism": {"score": 0},
        "free_trade_vs_isolationism": {"score": 0},
        "gun_control": {"score": 0},
        "immigration_border_wall_deportations": {"score": 0},
        "israel_vs_palestine": {"score": 0},
        "medicaid_cuts_vs_expansion": {"score": 0},
        "minimum_wage": {"score": 0},
        "obamacare_repeal_vs_expansion": {"score": 0},
        "same_sex_marriage": {"score": 0},
        "stock_trading_restrictions": {"score": 0},
        "vaccines_public_health_vs_health_skepticism": {"score": 0},
        "voter_id_and_election_restrictions": {
            "score": 2,
            "evidence": "The bill amends the National Voter Registration Act to require proof of United States citizenship to register to vote in elections for Federal office, and adds processes for those without documentary proof and in cases of discrepancies."
        }
    }
}

def validate_bill_classification(data):
    try:
        validated = BillClassification.model_validate_json(data)
        print("Valid JSON")
        print(validated.model_dump())
        return validated
        
    except ValidationError as e:
        print(e)
        return None
        #TODO: Rerun LLM and hope it works on the second time (if it fails again give up)
        