"""TC-034: Add Products to Compare List"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC034_AddCompare(BaseTest):
    TC_ID    = "TC-034"
    SUMMARY  = "Add Products to Compare List"
    MODULE   = "Product Compare & Reviews"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")
        # Use computers category which has more products with compare buttons
        page.goto(base + "computers", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Computers category page")

        # Try multiple selectors for compare button
        compare_btns = page.locator(
            "input[value='Add to compare list'], "
            "button:has-text('Add to compare list'), "
            ".add-to-compare-list-button, "
            "a:has-text('Add to compare')"
        )
        count = compare_btns.count()
        assert count >= 2, f"Less than 2 compare buttons found (found {count}) – try a different category"
        self.step_pass(page, 2, f"Verify compare buttons available – {count} found")

        compare_btns.nth(0).click()
        page.wait_for_timeout(1500)
        self.step_pass(page, 3, "Click Add to compare on first product")

        compare_btns.nth(1).click()
        page.wait_for_timeout(1500)
        self.step_pass(page, 4, "Click Add to compare on second product")

        compare_bar = page.locator(
            ".compare-products-bar, .block-compare, "
            "a:has-text('Compare'), #compare-products-bar"
        ).first
        expect(compare_bar).to_be_visible(timeout=8_000)
        self.step_pass(page, 5, "Verify compare bar/section visible")

        return "Pass", "Two products added to compare list successfully."

if __name__ == "__main__":
    r = TC034_AddCompare().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
