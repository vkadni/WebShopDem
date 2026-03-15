"""TC-005: Search with Invalid Keyword"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC005_SearchInvalid(BaseTest):
    TC_ID    = "TC-005"
    SUMMARY  = "Search with Invalid Keyword"
    MODULE   = "Search Functionality"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to home page")

        search = page.locator("input#small-searchterms, input[name='q'], .search-box input").first
        d = D.all_tc("TC-005")
        search.fill(d.get("search_keyword","xyzabc123notexist"))
        self.step_pass(page, 2, "Enter invalid keyword 'xyzabc123notexist'")

        page.locator("input.button-1.search-box-button, button[type='submit']").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Click Search button")

        body = page.locator("body").inner_text()
        assert any(phrase in body for phrase in [
            d.get("expected_message","No products were found"), "no products", "0 products"
        ]), "Expected 'no results' message not found"
        self.step_pass(page, 4, "Verify 'No products were found' message displayed")

        return "Pass", "Invalid keyword search correctly shows no results message."
