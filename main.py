"""
Credit Card Extractor - CLI Entry Point
----------------------------------------
Scrapes credit card URLs and exports structured data.

Usage:
    python main.py                    # Process all URLs in cards.json
    python main.py --provider openai  # Use OpenAI instead of Gemini
"""

import sys
import asyncio
import argparse
import json
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent / "src"))

from extractor import (
    CreditCard,
    LLMProvider,
    scrape_and_clean,
    extract_data,
    load_config,
)
from extractor.utils import load_urls, save_json


async def process_card(url: str, hint: str, provider: LLMProvider) -> CreditCard | None:
    """Process a single credit card URL"""
    try:
        print(f"\n{'─'*60}")
        print(f"📋 {hint}")
        print(f"{'─'*60}")
        
        markdown = await scrape_and_clean(url)
        card = extract_data(markdown, provider)
        return card
        
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        return None


async def main():
    parser = argparse.ArgumentParser(description="Credit Card Data Extractor")
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai"],
        default="gemini",
        help="LLM provider (default: gemini)"
    )
    parser.add_argument(
        "--input",
        default="cards.json",
        help="Input URLs file (default: cards.json)"
    )
    parser.add_argument(
        "--output",
        default="output.json",
        help="Output directory (default: output.json)"
    )
    args = parser.parse_args()
    
    provider = LLMProvider.GEMINI if args.provider == "gemini" else LLMProvider.OPENAI
    
    # Load configuration
    load_config()
    
    print("═" * 60)
    print("🚀 Credit Card Extractor")
    print("═" * 60)
    print(f"   Provider: {provider.value.upper()}")
    print(f"   Input: {args.input}")
    print(f"   Output: {args.output}/")
    
    # Load URLs
    urls = load_urls(args.input)
    print(f"   Cards: {len(urls)}")
    
    # Process each card
    results = []
    for idx, item in enumerate(urls, 1):
        card = await process_card(item["url"], item["card_hint"], provider)
        if card:
            results.append(card.model_dump())
        
        # Rate limiting between requests
        if idx < len(urls):
            await asyncio.sleep(2)
    
    # Export results
    print(f"\n{'═'*60}")
    if results:
        save_json(results, args.output)
        print(f"✅ Extracted {len(results)}/{len(urls)} cards")
    else:
        print("❌ No cards extracted")
    print("═" * 60)


if __name__ == "__main__":
    asyncio.run(main())
