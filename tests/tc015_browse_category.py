"""TC-015: Browse a Product Category"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC015_BrowseCategory(BaseTest):
    TC_ID    = "TC-015"
    SUMMARY  = "Browse a Product Category"
    MODULE   = "Product Browsing & Details"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to home page")

        page.locator("ul.top-menu a:has-text('Books'), .top-menu a:has-text('Books')").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Click Books category link")

        products = page.locator(".product-item, .item-box")
        count = products.count()
        assert count > 0, "No products found in Books category"
        self.step_pass(page, 3, f"Verify Books category page loaded – {count} product(s) visible")

        return "Pass", f"Books category loaded with {count} product(s)."
