"""TC-004: Search with Valid Keyword"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC004_SearchValid(BaseTest):
    TC_ID    = "TC-004"
    SUMMARY  = "Search with Valid Keyword"
    MODULE   = "Search Functionality"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to home page")

        search = page.locator("input#small-searchterms, input[name='q'], .search-box input").first
        d = D.all_tc("TC-004")
        search.fill(d.get("search_keyword","book"))
        self.step_pass(page, 2, "Enter keyword 'book' in search box")

        page.locator("input.button-1.search-box-button, button[type='submit']").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Click Search button")

        results = page.locator(".product-item, .item-box")
        count = results.count()
        assert count > 0, "No search results found for 'book'"
        self.step_pass(page, 4, f"Verify search results displayed – {count} product(s) found")

        return "Pass", f"Search for 'book' returned {count} product(s)."
