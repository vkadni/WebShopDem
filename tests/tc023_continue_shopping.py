"""TC-023: Continue Shopping from Cart"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC023_ContinueShopping(BaseTest):
    TC_ID    = "TC-023"
    SUMMARY  = "Continue Shopping from Cart"
    MODULE   = "Shopping Cart"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "cart", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Cart page")

        btn = page.locator("a:has-text('Continue shopping'), button:has-text('Continue shopping')")
        expect(btn.first).to_be_visible(timeout=5_000)
        self.step_pass(page, 2, "Verify Continue Shopping button visible")

        btn.first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Click Continue Shopping")

        assert page.url != BASE_URL + "cart", "Still on cart page after clicking continue shopping"
        self.step_pass(page, 4, f"Verify redirected away from cart – URL: {page.url}")

        return "Pass", f"Continue Shopping redirected to: {page.url}"
