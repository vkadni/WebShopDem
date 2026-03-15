"""TC-026: Proceed to Checkout as Guest"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC026_CheckoutGuest(BaseTest):
    TC_ID    = "TC-026"
    SUMMARY  = "Proceed to Checkout as Guest"
    MODULE   = "Checkout Process"
    PRIORITY = "Critical"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")
        page.goto(base + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 1, "Add product to cart as precondition")

        page.goto(base + "cart", wait_until="domcontentloaded")
        page.locator("button:has-text('Checkout'), input[value='Checkout']").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Click Checkout button from cart")

        # Handle guest checkout option if shown
        guest_btn = page.locator(
            "input[value='Checkout as Guest'], "
            "button:has-text('Checkout as Guest'), "
            ".checkout-as-guest-button"
        )
        if guest_btn.count() > 0:
            guest_btn.first.click()
            page.wait_for_load_state("networkidle")
            self.step_pass(page, 3, "Selected Checkout as Guest option")
        else:
            self.step_pass(page, 3, "Already on checkout page – guest checkout direct")

        # Verify checkout page loaded – look for any checkout step indicator
        checkout_indicator = page.locator(
            ".checkout-page, "
            ".opc-wrapper, "
            "#checkout-steps, "
            "form[action*='checkout'], "
            ".step-title"
        ).first
        expect(checkout_indicator).to_be_visible(timeout=10_000)
        self.step_pass(page, 4, "Verify checkout page loaded successfully")

        return "Pass", "Checkout page loaded for guest user."

if __name__ == "__main__":
    r = TC026_CheckoutGuest().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
