"""
LLM Extraction Module
--------------------
Gemini and OpenAI integration for structured data extraction.
"""

import os
import json
from .models import CreditCard, LLMProvider
from .utils import generate_card_id


EXTRACTION_PROMPT = """You are an expert data extractor for Indian credit cards.
Extract comprehensive details from the website content into the JSON schema.

RULES:
- Generate unique ID from bank + card name (e.g., "hdfc-infinia-metal")
- Extract numeric values without currency symbols
- Detect card network from mentions of Visa/Mastercard/Amex/Rupay/Diners
- Extract category-specific reward multipliers
- Extract benefits with icon suggestions, title, description
- Parse milestone benefits with spend thresholds
- Suggest colors based on card tier (premium=#d4af37, travel=#3b82f6, lifestyle=#8b5cf6)

SCHEMA:
{
  "id": "unique-identifier",
  "name": "Card name",
  "bank": "Bank name",
  "network": "Visa|Mastercard|Amex|Rupay|Diners|Unknown",
  "annualFee": <number>,
  "joiningFee": <number>,
  "rewardRate": <points per Rs 100>,
  "rewards": {"dining": <n>, "travel": <n>, "fuel": <n>, "grocery": <n>, "shopping": <n>, "utilities": <n>, "entertainment": <n>, "international": <n>},
  "color": "#hexcolor",
  "accentColor": "#hexcolor",
  "gradient": "linear-gradient(...)",
  "benefits": [{"icon": "icon-name", "title": "...", "description": "..."}],
  "milestones": [{"spend": <amount>, "benefit": "...", "value": <inr>}],
  "bestMerchants": [{"name": "...", "logo": "", "multiplier": "..."}],
  "rewardPointValue": <value per point>,
  "rewardPointsName": "Points name",
  "mostlyUsedFor": ["Category1", "Category2"]
}

Return ONLY valid JSON, no markdown."""


def _get_gemini_client():
    """Get configured Gemini client"""
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=EXTRACTION_PROMPT)


def _get_openai_client():
    """Get configured OpenAI client"""
    from openai import OpenAI
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _extract_with_gemini(markdown: str) -> CreditCard:
    """Extract using Google Gemini"""
    model = _get_gemini_client()
    
    prompt = f"Content:\n{markdown[:15000]}"
    response = model.generate_content(prompt)
    
    text = response.text.strip()
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:].strip()
    
    data = json.loads(text)
    return CreditCard(**data)


def _extract_with_openai(markdown: str) -> CreditCard:
    """Extract using OpenAI GPT"""
    client = _get_openai_client()
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": f"Extract from:\n\n{markdown[:15000]}"}
        ],
        response_format=CreditCard,
    )
    
    card = completion.choices[0].message.parsed
    if not card.id or card.id == "string":
        card.id = generate_card_id(card.bank, card.name)
    
    return card


def extract_data(markdown: str, provider: LLMProvider = LLMProvider.GEMINI) -> CreditCard:
    """
    Extract credit card data using LLM.
    
    Args:
        markdown: Cleaned markdown text from webpage
        provider: LLM provider (GEMINI or OPENAI)
        
    Returns:
        Validated CreditCard model
    """
    print(f"   🤖 Extracting with {provider.value.upper()}...")
    
    if provider == LLMProvider.GEMINI:
        card = _extract_with_gemini(markdown)
    else:
        card = _extract_with_openai(markdown)
    
    print(f"   ✅ Extracted: {card.name}")
    return card
