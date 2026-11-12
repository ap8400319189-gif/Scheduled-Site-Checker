import re
import sys
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

APP_URL = "https://lecture-summ-ai.streamlit.app/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(APP_URL, timeout=60_000)

    wake_button = page.get_by_role("button", name=re.compile("get this app back up", re.I))
    try:
        wake_button.click(timeout=15_000)
        print("App was asleep - woke it up.")
    except PWTimeout:
        print("App already awake.")

    app = page.frame_locator("iframe[title='streamlitApp']").locator("[data-testid='stApp']")
    try:
        app.wait_for(state="attached", timeout=120_000)
        print("App loaded.")
    except PWTimeout:
        sys.exit("ERROR: app did not load within 2 minutes.")

    page.wait_for_timeout(15_000)
    browser.close()
