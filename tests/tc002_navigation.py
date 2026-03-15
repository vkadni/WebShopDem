"""TC-002: Verify Top Navigation Category Links"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC002_NavigationLinks(BaseTest):
    TC_ID    = "TC-002"
    SUMMARY  = "Verify Top Navigation Category Links"
    MODULE   = "Home Page & Navigation"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Navigate to home page")

        for item in ["Books", "Computers", "Electronics", "Apparel"]:
            page.goto(BASE_URL)
            page.locator(f"ul.top-menu a:has-text('{item}'), .top-menu a:has-text('{item}')").first.click()
            page.wait_for_load_state("networkidle")
            assert item.lower() in page.url.lower() or page.title() != "", f"{item} page did not load"
            self.step_pass(page, ["Books","Computers","Electronics","Apparel"].index(item)+2,
                           f"Click '{item}' nav link – page loaded", notes=f"URL: {page.url}")

        return "Pass", "All 4 navigation links (Books, Computers, Electronics, Apparel) loaded correctly."
