"""TC-020: View Shopping Cart"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC020_ViewCart(BaseTest):
    TC_ID    = "TC-020"
    SUMMARY  = "View Shopping Cart"
    MODULE   = "Shopping Cart"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        # Add item first
        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 1, "Add a product to cart as precondition")

        page.goto(BASE_URL + "cart", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to Shopping Cart page")

        cart_items = page.locator(".cart-item-row, tr.cart-item")
        assert cart_items.count() > 0, "Cart is empty – no items found"
        self.step_pass(page, 3, f"Verify cart contains {cart_items.count()} item(s)")

        price = page.locator(".product-subtotal, .cart-total, .order-subtotal")
        expect(price.first).to_be_visible(timeout=5_000)
        self.step_pass(page, 4, "Verify price/subtotal visible in cart")

        return "Pass", f"Cart page shows {cart_items.count()} item(s) with price details."
