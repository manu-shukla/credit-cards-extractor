"""
Utility Functions
-----------------
Configuration loading, ID generation, and helpers.
"""

import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv


def load_config():
    """Load environment variables from .env file"""
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing API key. Set GEMINI_API_KEY or OPENAI_API_KEY in .env")


def generate_card_id(bank: str, card_name: str) -> str:
    """Generate a unique card ID from bank and card name"""
    combined = f"{bank}-{card_name}"
    card_id = re.sub(r'[^a-z0-9-]', '', combined.lower().replace(' ', '-'))
    card_id = re.sub(r'-+', '-', card_id)
    return card_id.strip('-')


def load_urls(filepath: str = "cards.json") -> list:
    """Load URLs from JSON config file"""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {filepath}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: list, filepath: str):
    """Save data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
