"""TC-017: Verify Product Price Display"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC017_ProductPrice(BaseTest):
    TC_ID    = "TC-017"
    SUMMARY  = "Verify Product Price Display"
    MODULE   = "Product Browsing & Details"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Books category page")

        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Open first product detail page")

        price_el = page.locator(".price, .product-price, [itemprop='price']").first
        expect(price_el).to_be_visible(timeout=5_000)
        price_text = price_el.inner_text()
        assert any(c in price_text for c in ["$","£","€","USD","GBP"]) or price_text.replace(".","").replace(",","").strip().isdigit(), \
            f"Price does not contain currency symbol: '{price_text}'"
        self.step_pass(page, 3, f"Verify price displayed with currency – '{price_text}'")

        return "Pass", f"Product price displayed correctly: '{price_text}'."
