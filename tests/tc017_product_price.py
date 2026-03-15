"""TC-017: Verify Product Price Display"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC017_ProductPrice(BaseTest):
    TC_ID    = "TC-017"
    SUMMARY  = "Verify Product Price Display"
    MODULE   = "Product Browsing & Details"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(D.config("base_url") + D.tc(self.TC_ID, "category_url", "books"),
                  wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Books category page")

        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Open first product detail page")

        price_el = page.locator(".price.actual-price, .product-price, [itemprop='price'], .price").first
        expect(price_el).to_be_visible(timeout=5_000)
        price_text = price_el.inner_text().strip()

        # Site shows "10.00" or "Price: 10.00" — just verify it is not empty and numeric
        assert price_text != "", "Price element is empty"
        assert any(c.isdigit() for c in price_text), \
            f"Price does not contain a number: '{price_text}'"
        self.step_pass(page, 3, f"Verify price displayed – '{price_text}'")

        return "Pass", f"Product price displayed correctly: '{price_text}'."

if __name__ == "__main__":
    r = TC017_ProductPrice().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
