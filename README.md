# Credit Card Extractor 💳

Extract structured credit card data from Indian bank websites using AI.

## Features

- **Web Scraping** - Playwright-based with fallback strategies
- **LLM Extraction** - Gemini (default) or OpenAI
- **TypeScript Export** - Ready for frontend integration
- **Robust Handling** - Retries, timeouts, validation

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Configure API key
cp .env.example .env
# Edit .env: GEMINI_API_KEY=your_key

# Add your URLs to cards.json
# Run extractor
python main.py
```

## Usage

```bash
# Process all URLs in cards.json
python main.py

# Use OpenAI instead of Gemini
python main.py --provider openai

# Custom input/output
python main.py --input my_cards.json --output ./dist
```

## Configuration

### cards.json
```json
[
  {
    "url": "https://www.hdfcbank.com/...",
    "card_hint": "HDFC Infinia"
  }
]
```

### .env
```
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key  # optional
```

## Output

Results are exported to root directory
- `cards.json` - Raw JSON data


## Project Structure

```
├── main.py              # CLI entry point
├── src/extractor/       # Core package
│   ├── models.py        # Pydantic schemas
│   ├── scraper.py       # Web scraping
│   ├── llm.py           # LLM extraction
│   └── utils.py         # Utilities
├── cards.json           # Input URLs
```

## License

MIT
