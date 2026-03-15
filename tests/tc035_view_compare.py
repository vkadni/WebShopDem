"""TC-035: View Product Comparison Page"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC035_ViewCompare(BaseTest):
    TC_ID    = "TC-035"
    SUMMARY  = "View Product Comparison Page"
    MODULE   = "Product Compare & Reviews"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")

        # Add 2 products from computers category
        page.goto(base + "computers", wait_until="domcontentloaded")
        compare_btns = page.locator(
            "input[value='Add to compare list'], "
            ".add-to-compare-list-button, "
            "a:has-text('Add to compare')"
        )
        assert compare_btns.count() >= 2, "Not enough products to compare"
        compare_btns.nth(0).click()
        page.wait_for_timeout(1000)
        compare_btns.nth(1).click()
        page.wait_for_timeout(1000)
        self.step_pass(page, 1, "Add two products to compare as precondition")

        page.goto(base + "compareproducts", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to Compare Products page")

        compare_table = page.locator(
            ".compare-products-table, table.compare, "
            ".product-compare-page table, "
            "#product-comparison"
        ).first
        expect(compare_table).to_be_visible(timeout=8_000)
        self.step_pass(page, 3, "Verify comparison table displayed")

        cols = page.locator(
            ".compare-products-table td.product, "
            ".compare th.product, "
            ".product-compare-page td[class*='product']"
        )
        assert cols.count() >= 2, "Less than 2 products shown in comparison"
        self.step_pass(page, 4, f"Verify {cols.count()} products shown side-by-side")

        return "Pass", f"Compare page shows {cols.count()} products in table."

if __name__ == "__main__":
    r = TC035_ViewCompare().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
