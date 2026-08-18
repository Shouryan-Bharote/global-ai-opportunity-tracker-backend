"""Debug script: dumps Unstop's page structure to find the correct card selectors."""
import asyncio
import re

from patchright.async_api import async_playwright


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Navigating to unstop.com/hackathons ...")
        await page.goto("https://unstop.com/hackathons", wait_until="domcontentloaded")

        # Wait a bit for JS to render cards
        await asyncio.sleep(5)

        html = await page.content()
        print(f"Page HTML length: {len(html)} chars\n")

        # Save the full HTML for manual inspection
        with open("unstop_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved full HTML to unstop_page.html\n")

        # Try to find repeating patterns that look like cards
        # Look for elements with class names containing common card keywords
        candidates = re.findall(
            r'class="([^"]*(?:card|item|listing|opportunity|hackathon|competition)[^"]*)"',
            html,
            re.IGNORECASE,
        )

        # Deduplicate and show most frequent class names
        from collections import Counter
        counts = Counter(candidates)
        print("=== Top repeating class patterns (likely card containers) ===")
        for cls, count in counts.most_common(20):
            print(f"  [{count:3d}x] .{cls.split()[0]}")

        # Also check what tags exist around 'hackathon' keyword
        print("\n=== Snippets around 'hackathon' keyword ===")
        for match in re.finditer(r'.{0,150}hackathon.{0,150}', html, re.IGNORECASE):
            snippet = match.group().strip().replace('\n', ' ')
            if 'class' in snippet.lower():
                print(f"  {snippet[:200]}")
                print()

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
