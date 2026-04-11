from typing import Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict


class CategoryScore(BaseModel):
    score: int = Field(..., ge=-2, le=2)
    evidence: Optional[str] = None


class Categories(BaseModel):
    abortion: CategoryScore
    affirmative_action: CategoryScore
    balanced_budget_vs_expand_spending: CategoryScore
    citizenship_pathways: CategoryScore
    clean_energy_vs_fossil_fuels: CategoryScore
    corporate_tax_rates: CategoryScore
    crypto_gambling_corruption_regulation: CategoryScore
    executive_power_limits: CategoryScore
    foreign_aid_vs_isolationism: CategoryScore
    free_trade_vs_isolationism: CategoryScore
    gun_control: CategoryScore
    immigration_border_wall_deportations: CategoryScore
    israel_vs_palestine: CategoryScore
    medicaid_cuts_vs_expansion: CategoryScore
    minimum_wage: CategoryScore
    obamacare_repeal_vs_expansion: CategoryScore
    same_sex_marriage: CategoryScore
    stock_trading_restrictions: CategoryScore
    vaccines_public_health_vs_health_skepticism: CategoryScore
    voter_id_and_election_restrictions: CategoryScore

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

try:
    validated = BillClassification.model_validate(data)
    print("Valid JSON")
    print(validated.model_dump())
except ValidationError as e:
    print("Validation failed")
    #TODO: Rerun LLM and hope it works on the second time (if it fails again give up)
    print(e)