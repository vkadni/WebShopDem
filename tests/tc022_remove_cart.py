"""TC-022: Remove Item from Cart"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC022_RemoveCart(BaseTest):
    TC_ID    = "TC-022"
    SUMMARY  = "Remove Item from Cart"
    MODULE   = "Shopping Cart"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 1, "Add product to cart as precondition")

        page.goto(BASE_URL + "cart", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to Cart page")

        page.locator("input.remove-btn, td.remove-from-cart input").first.check()
        self.step_pass(page, 3, "Check the Remove checkbox for item")

        page.locator("input[name='updatecart'], button:has-text('Update')").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 4, "Click Update Shopping Cart")

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["Your Shopping Cart is empty", "cart is empty", "no items"]), \
            "Cart not empty after removal"
        self.step_pass(page, 5, "Verify cart is empty after item removal")

        return "Pass", "Item removed from cart. Empty cart message displayed."
