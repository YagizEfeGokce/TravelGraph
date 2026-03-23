"""Take screenshots of TravelGraph pages using Playwright."""

import asyncio
import json
import urllib.request
from pathlib import Path

from playwright.async_api import async_playwright

SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

FRONTEND = "http://localhost:5173"
BACKEND = "http://localhost:8000"


async def screenshot(page, path: str, url: str, wait_ms: int = 2000) -> None:
    print(f"  → Navigating to {url}")
    await page.goto(url, wait_until="networkidle", timeout=15000)
    await page.wait_for_timeout(wait_ms)
    await page.screenshot(path=str(SCREENSHOTS_DIR / path), full_page=True)
    print(f"  ✓ Saved {path}")


def get_first_destination_id() -> str | None:
    try:
        with urllib.request.urlopen(f"{BACKEND}/api/destinations?limit=1", timeout=5) as r:
            data = json.loads(r.read())
            # Handle both list and {"items": [...]} shapes
            items = data if isinstance(data, list) else data.get("items", data.get("destinations", []))
            if items:
                return items[0].get("id")
    except Exception as e:
        print(f"  ! Could not fetch destinations: {e}")
    return None


async def main() -> None:
    dest_id = get_first_destination_id()
    print(f"First destination ID: {dest_id}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await context.new_page()

        # Suppress console noise
        page.on("console", lambda _: None)

        print("\n[1/6] Home page")
        await screenshot(page, "home.png", FRONTEND)

        print("[2/6] Explore page")
        await screenshot(page, "explore.png", f"{FRONTEND}/explore")

        print("[3/6] Destination detail")
        if dest_id:
            await screenshot(page, "destination-detail.png", f"{FRONTEND}/destinations/{dest_id}")
        else:
            # Fallback: take screenshot of explore with a note
            await screenshot(page, "destination-detail.png", f"{FRONTEND}/explore")
            print("  ! No destination ID found, used /explore as fallback")

        print("[4/6] Festivals page")
        await screenshot(page, "festivals.png", f"{FRONTEND}/festivals")

        print("[5/6] Login page")
        await screenshot(page, "login.png", f"{FRONTEND}/login")

        print("[6/6] API docs")
        await screenshot(page, "api-docs.png", f"{BACKEND}/docs")

        await browser.close()

    print("\n✅ All screenshots saved to screenshots/")
    for f in sorted(SCREENSHOTS_DIR.glob("*.png")):
        size_kb = f.stat().st_size // 1024
        print(f"   {f.name}  ({size_kb} KB)")


if __name__ == "__main__":
    asyncio.run(main())
