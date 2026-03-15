"""TC-019: Add Product to Cart"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC019_AddToCart(BaseTest):
    TC_ID    = "TC-019"
    SUMMARY  = "Add Product to Cart"
    MODULE   = "Shopping Cart"
    PRIORITY = "Critical"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Books category")

        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Open first product detail page")

        before = page.locator(".cart-qty, #topcartlink .count").first.inner_text() if \
            page.locator(".cart-qty, #topcartlink .count").count() > 0 else "0"

        page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 3, "Click Add to Cart button")

        notif = page.locator(".bar-notification, .success, #bar-notification")
        expect(notif.first).to_be_visible(timeout=8_000)
        self.step_pass(page, 4, "Verify success notification displayed")

        return "Pass", "Product added to cart. Success notification shown."
