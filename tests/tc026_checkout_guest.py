"""TC-026: Proceed to Checkout as Guest"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC026_CheckoutGuest(BaseTest):
    TC_ID    = "TC-026"
    SUMMARY  = "Proceed to Checkout as Guest"
    MODULE   = "Checkout Process"
    PRIORITY = "Critical"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 1, "Add product to cart as precondition")

        page.goto(BASE_URL + "cart", wait_until="domcontentloaded")
        page.locator("button:has-text('Checkout'), input[value='Checkout']").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Click Checkout button from cart")

        guest_btn = page.locator("input[value='Checkout as Guest'], button:has-text('Checkout as Guest')")
        if guest_btn.count() > 0:
            guest_btn.first.click()
            page.wait_for_load_state("networkidle")
            self.step_pass(page, 3, "Click Checkout as Guest option")
        else:
            self.step_pass(page, 3, "Already on checkout page (guest option not prompted)")

        billing = page.locator("#billing-address-select, #BillingNewAddress_FirstName, .billing-address")
        expect(billing.first).to_be_visible(timeout=8_000)
        self.step_pass(page, 4, "Verify billing address form displayed on checkout page")

        return "Pass", "Checkout as guest loaded billing address form successfully."
