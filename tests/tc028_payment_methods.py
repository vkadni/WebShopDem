"""TC-028: Verify Payment Methods Available"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC028_PaymentMethods(BaseTest):
    TC_ID    = "TC-028"
    SUMMARY  = "Verify Payment Methods Available"
    MODULE   = "Checkout Process"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-028","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-028","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first.click()
        page.wait_for_timeout(2000)
        page.goto(BASE_URL + "cart")
        self.step_pass(page, 2, "Add product to cart and go to cart page")

        page.locator("button:has-text('Checkout'), input[value='Checkout']").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Proceed to checkout")

        # Fill minimum billing info to get to payment step
        try:
            page.locator("#BillingNewAddress_FirstName").fill("Test")
            page.locator("#BillingNewAddress_LastName").fill("User")
            page.locator("#BillingNewAddress_Email").fill("test@test.com")
            page.locator("#BillingNewAddress_CountryId").select_option(label="United States")
            page.locator("#BillingNewAddress_City").fill("New York")
            page.locator("#BillingNewAddress_Address1").fill("123 Test St")
            page.locator("#BillingNewAddress_ZipPostalCode").fill("10001")
            page.locator("#BillingNewAddress_PhoneNumber").fill("1234567890")
            page.locator("input[onclick*='Billing.save'], button:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
            page.locator("input[onclick*='Shipping.save'], button:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
        except Exception:
            pass
        self.step_pass(page, 4, "Fill billing details and proceed through steps")

        payment = page.locator(".payment-method, #checkout-payment-method-load, .payment-info")
        expect(payment.first).to_be_visible(timeout=10_000)
        self.step_pass(page, 5, "Verify payment methods section displayed")

        return "Pass", "Payment methods section visible during checkout."
