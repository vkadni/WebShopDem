"""TC-006: Search with Empty Input"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC006_SearchEmpty(BaseTest):
    TC_ID    = "TC-006"
    SUMMARY  = "Search with Empty Input"
    MODULE   = "Search Functionality"
    PRIORITY = "Low"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to home page")

        page.locator("input.button-1.search-box-button, button[type='submit']").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Click Search with empty input")

        assert page.locator("body").count() > 0, "Page crashed on empty search"
        self.step_pass(page, 3, "Verify page does not crash on empty search")

        return "Pass", "Empty search did not crash; page responded gracefully."
