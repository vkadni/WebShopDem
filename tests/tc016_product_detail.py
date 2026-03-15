"""TC-016: View Product Detail Page"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC016_ProductDetail(BaseTest):
    TC_ID    = "TC-016"
    SUMMARY  = "View Product Detail Page"
    MODULE   = "Product Browsing & Details"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Books category page")

        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Click first product to open detail page")

        title = page.locator(".product-name h1, h1.productTitle").first
        expect(title).to_be_visible(timeout=8_000)
        self.step_pass(page, 3, "Verify product name/title visible")

        price = page.locator(".price, .product-price, [itemprop='price']").first
        expect(price).to_be_visible(timeout=5_000)
        self.step_pass(page, 4, "Verify product price visible")

        add_to_cart = page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first
        expect(add_to_cart).to_be_visible(timeout=5_000)
        self.step_pass(page, 5, "Verify Add to Cart button visible")

        return "Pass", "Product detail page loaded with name, price, and Add to Cart button."
