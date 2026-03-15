"""TC-034: Add Products to Compare List"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC034_AddCompare(BaseTest):
    TC_ID    = "TC-034"
    SUMMARY  = "Add Products to Compare List"
    MODULE   = "Product Compare & Reviews"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Books category page")

        compare_btns = page.locator("input[value='Add to compare list'], button:has-text('Add to compare list')")
        assert compare_btns.count() >= 2, "Less than 2 products available to compare"
        self.step_pass(page, 2, f"Verify at least 2 products available – found {compare_btns.count()}")

        compare_btns.nth(0).click()
        page.wait_for_timeout(1500)
        self.step_pass(page, 3, "Click 'Add to compare list' on first product")

        compare_btns.nth(1).click()
        page.wait_for_timeout(1500)
        self.step_pass(page, 4, "Click 'Add to compare list' on second product")

        compare_bar = page.locator(".compare-products-bar, .block-compare, a:has-text('Compare')")
        expect(compare_bar.first).to_be_visible(timeout=8_000)
        self.step_pass(page, 5, "Verify compare bar/section appears with products")

        return "Pass", "Two products added to compare list. Compare bar visible."
