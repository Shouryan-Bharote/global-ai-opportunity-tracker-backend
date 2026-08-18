"""Inspect app-pagination element."""
import asyncio
from patchright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://unstop.com/hackathons", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        pag = page.locator("app-pagination")
        if await pag.count() > 0:
            print("=== app-pagination outer HTML ===")
            print(await pag.evaluate("el => el.outerHTML"))
        else:
            print("app-pagination not found!")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
