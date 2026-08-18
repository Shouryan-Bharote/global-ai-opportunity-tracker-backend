import asyncio
from patchright.async_api import async_playwright

async def check_pages():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        url = 'https://devpost.com/hackathons?challenge_type[]=online&challenge_type[]=in-person&open_to[]=public&status[]=upcoming&status[]=open&themes[]=Machine%20Learning%2FAI'
        await page.goto(url)
        await page.wait_for_timeout(3000)
        
        cards = await page.locator('.hackathon-tile').count()
        print(f'Initial load: found {cards} cards')
        
        for i in range(5):
            await page.keyboard.press("End")
            await page.wait_for_timeout(2000)
            cards = await page.locator('.hackathon-tile').count()
            print(f'After press End {i+1}: found {cards} cards')
            
        texts = await page.locator('.hackathon-tile h3').all_inner_texts()
        print('Cards:')
        for t in texts:
            print('  -', t)

asyncio.run(check_pages())
