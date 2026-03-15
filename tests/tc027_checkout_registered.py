"""TC-027: Checkout as Registered User"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC027_CheckoutRegistered(BaseTest):
    TC_ID    = "TC-027"
    SUMMARY  = "Checkout as Registered User"
    MODULE   = "Checkout Process"
    PRIORITY = "Critical"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")
        page.goto(base + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc(self.TC_ID, "email", D.config("admin_email")))
        page.locator("#Password").fill(D.tc(self.TC_ID, "password", D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(base + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 2, "Add product to cart")

        page.goto(base + "cart", wait_until="domcontentloaded")
        page.locator("button:has-text('Checkout'), input[value='Checkout']").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Proceed to Checkout")

        # Verify checkout page loaded
        checkout_indicator = page.locator(
            ".checkout-page, "
            ".opc-wrapper, "
            "#checkout-steps, "
            "form[action*='checkout'], "
            ".step-title"
        ).first
        expect(checkout_indicator).to_be_visible(timeout=10_000)
        self.step_pass(page, 4, "Verify checkout page loaded for registered user")

        return "Pass", "Registered user checkout page loaded successfully."

if __name__ == "__main__":
    r = TC027_CheckoutRegistered().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
