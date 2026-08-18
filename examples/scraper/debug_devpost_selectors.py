"""Debug script to inspect Devpost live page structure and selectors."""
import asyncio
from patchright.async_api import async_playwright


async def main() -> None:
    url = "https://devpost.com/hackathons?search=artificial+intelligence&challenge_type[]=online"
    print(f"Navigating to {url}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)

        html = await page.content()
        with open("devpost_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Saved devpost_page.html (Length: {len(html)})")

        tiles = page.locator(".hackathon-tile, [class*='hackathon-tile'], .challenge-listing")
        print(f"Tiles count: {await tiles.count()}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
