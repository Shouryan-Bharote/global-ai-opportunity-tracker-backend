import asyncio
from patchright.async_api import async_playwright

async def get_screenshot():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        url = 'https://devpost.com/hackathons?challenge_type[]=online&challenge_type[]=in-person&open_to[]=public&status[]=upcoming&status[]=open'
        await page.goto(url)
        await page.wait_for_timeout(3000)
        
        # Scroll 1
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await page.wait_for_timeout(3000)
        
        # Scroll 2
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await page.wait_for_timeout(3000)
        
        # Take screenshot of the bottom
        await page.screenshot(path='devpost_bottom.png', full_page=True)
        await browser.close()

asyncio.run(get_screenshot())
