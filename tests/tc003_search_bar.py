"""TC-003: Verify Search Bar Visibility"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC003_SearchBarVisibility(BaseTest):
    TC_ID    = "TC-003"
    SUMMARY  = "Verify Search Bar Visibility"
    MODULE   = "Home Page & Navigation"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Navigate to home page")

        search = page.locator("input#small-searchterms, input[name='q'], .search-box input").first
        expect(search).to_be_visible(timeout=8_000)
        self.step_pass(page, 2, "Verify search bar is visible in header")

        expect(search).to_be_enabled()
        self.step_pass(page, 3, "Verify search bar is interactive/enabled")

        return "Pass", "Search bar is visible and interactive in the header."
