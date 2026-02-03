"""
Web Scraper Module
------------------
Playwright-based scraper with fallback strategies for bank websites.
"""

import html2text
from playwright.async_api import async_playwright


async def scrape_and_clean(url: str) -> str:
    """
    Scrape a credit card webpage and convert to clean Markdown.
    Uses multiple fallback strategies for difficult websites.
    
    Args:
        url: Credit card webpage URL
        
    Returns:
        Clean markdown text optimized for LLM processing
    """
    print(f"🌐 Scraping: {url}")
    
    strategies = [
        ('networkidle', 60000, 'network idle'),
        ('domcontentloaded', 45000, 'DOM content loaded'),
        ('load', 45000, 'page load'),
    ]
    
    cleaned_html = ""
    last_error = None
    
    for attempt, (wait_until, timeout, description) in enumerate(strategies, 1):
        try:
            print(f"   ⏳ Strategy {attempt}: {description}...")
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    locale='en-IN',
                    timezone_id='Asia/Kolkata',
                )
                page = await context.new_page()
                
                try:
                    await page.goto(url, wait_until=wait_until, timeout=timeout)
                    await page.wait_for_timeout(3000)
                    
                    # Remove unwanted elements
                    await page.evaluate("""
                        () => {
                            const selectorsToRemove = [
                                'script', 'style', 'nav', 'header', 'footer',
                                'iframe', 'noscript', '.cookie-banner', '.advertisement',
                                '#header', '#footer', '#navigation', '.sidebar',
                                '[class*="cookie"]', '[id*="cookie"]',
                                '[class*="banner"]', '[class*="popup"]'
                            ];
                            selectorsToRemove.forEach(selector => {
                                document.querySelectorAll(selector).forEach(el => el.remove());
                            });
                        }
                    """)
                    
                    cleaned_html = await page.content()
                    print(f"   ✅ Success with {description}")
                    break
                    
                finally:
                    await browser.close()
                    
        except Exception as e:
            last_error = e
            print(f"   ⚠️  {description} failed: {str(e)[:80]}")
            if attempt == len(strategies):
                raise Exception(f"All strategies failed. Last error: {last_error}")
    
    # Convert to Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0
    h.skip_internal_links = True
    
    markdown = h.handle(cleaned_html)
    markdown = '\n'.join(line for line in markdown.split('\n') if line.strip())
    
    print(f"   📝 Converted to Markdown ({len(markdown)} chars)")
    return markdown
