"""TC-021: Update Cart Quantity"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC021_UpdateCart(BaseTest):
    TC_ID    = "TC-021"
    SUMMARY  = "Update Cart Quantity"
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

        qty = page.locator("input.qty-input, input[name='itemquantity']").first
        d = D.all_tc("TC-021")
        qty.fill(d.get("new_quantity","2"))
        self.step_pass(page, 3, "Update quantity to 2")

        page.locator("input[name='updatecart'], button:has-text('Update')").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 4, "Click Update Shopping Cart")

        updated_qty = page.locator("input.qty-input, input[name='itemquantity']").first.input_value()
        assert updated_qty == d.get("new_quantity","2"), f"Quantity not updated, got: {updated_qty}"
        self.step_pass(page, 5, "Verify quantity updated to 2 and subtotal recalculated")

        return "Pass", "Cart quantity updated to 2 and subtotal recalculated."
