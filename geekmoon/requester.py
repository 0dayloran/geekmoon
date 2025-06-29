import asyncio
from pyppeteer import launch

async def fetch(url, browser):
    page = await browser.newPage()
    try:
        await page.goto(url, {'waitUntil' : 'domcontentloaded'})
        content = await page.content()
        final_url = page.url
        return content, final_url
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None
    finally:
        await page.close()

async def get_browser():
    return await launch(headless=True, args=['--no-sandbox'])