import asyncio
import time
from playwright.async_api import async_playwright, TimeoutError

async def run(url, output_file):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=30000)  # Set a timeout of 30 seconds
        except TimeoutError:
            print(f"TimeoutError: Failed to load {url} within the timeout period.")
        time.sleep(5)  # Wait for 5 seconds
        content = await page.content()
        with open(output_file, 'w') as f:
            f.write(content)
        await browser.close()

if __name__ == "__main__":
    url = 'https://www.showboxmovies.net/watch-movie/captain-america-brave-new-world-120751.10942312'
    output_file = './tools/output.html'
    
    asyncio.run(run(url, output_file))