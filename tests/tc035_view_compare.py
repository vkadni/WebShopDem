"""TC-035: View Product Comparison Page"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC035_ViewCompare(BaseTest):
    TC_ID    = "TC-035"
    SUMMARY  = "View Product Comparison Page"
    MODULE   = "Product Compare & Reviews"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        # Add 2 products to compare first
        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        compare_btns = page.locator("input[value='Add to compare list'], button:has-text('Add to compare list')")
        compare_btns.nth(0).click()
        page.wait_for_timeout(1000)
        compare_btns.nth(1).click()
        page.wait_for_timeout(1000)
        self.step_pass(page, 1, "Add two products to compare list as precondition")

        page.goto(BASE_URL + "compareproducts", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to Compare Products page")

        compare_table = page.locator(".compare-products-table, table.compare")
        expect(compare_table.first).to_be_visible(timeout=8_000)
        self.step_pass(page, 3, "Verify comparison table displayed")

        cols = page.locator(".compare-products-table th, .compare th")
        assert cols.count() >= 2, "Less than 2 products in comparison table"
        self.step_pass(page, 4, f"Verify {cols.count()} products shown side-by-side in comparison")

        return "Pass", f"Compare page shows {cols.count()} products in side-by-side table."
