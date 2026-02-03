"""
Credit Card Extractor Package
-----------------------------
Extract structured credit card data from Indian bank websites.
"""

from .models import (
    CreditCard,
    RewardCategory,
    Benefit,
    Milestone,
    BestMerchant,
    LLMProvider,
)
from .scraper import scrape_and_clean
from .llm import extract_data
from .utils import generate_card_id, load_config

__version__ = "1.0.0"
__all__ = [
    "CreditCard",
    "RewardCategory", 
    "Benefit",
    "Milestone",
    "BestMerchant",
    "LLMProvider",
    "scrape_and_clean",
    "extract_data",
    "generate_card_id",
    "load_config",
]
