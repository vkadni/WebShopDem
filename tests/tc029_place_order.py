"""TC-029: Complete Order Placement"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC029_PlaceOrder(BaseTest):
    TC_ID    = "TC-029"
    SUMMARY  = "Complete Order Placement"
    MODULE   = "Checkout Process"
    PRIORITY = "Critical"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-029","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-029","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 2, "Add product to cart")

        page.goto(BASE_URL + "cart")
        page.locator("button:has-text('Checkout'), input[value='Checkout']").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Proceed to Checkout")

        try:
            page.locator("#BillingNewAddress_FirstName").fill("Smoke")
            page.locator("#BillingNewAddress_LastName").fill("Tester")
            page.locator("#BillingNewAddress_Email").fill("smoke@test.com")
            page.locator("#BillingNewAddress_CountryId").select_option(label="United States")
            page.locator("#BillingNewAddress_City").fill("New York")
            page.locator("#BillingNewAddress_Address1").fill("123 Test St")
            page.locator("#BillingNewAddress_ZipPostalCode").fill("10001")
            page.locator("#BillingNewAddress_PhoneNumber").fill("1234567890")
            page.locator("input[onclick*='Billing.save'], .button-1:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
            self.step_pass(page, 4, "Fill billing address and continue")

            page.locator("input[onclick*='Shipping.save'], .button-1:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
            self.step_pass(page, 5, "Select shipping method and continue")

            page.locator("input[onclick*='PaymentMethod.save'], .button-1:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
            self.step_pass(page, 6, "Select payment method and continue")

            page.locator("input[onclick*='PaymentInfo.save'], .button-1:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
            self.step_pass(page, 7, "Confirm payment info and continue")

            page.locator("input[onclick*='Confirm.save'], button:has-text('Confirm')").first.click()
            page.wait_for_load_state("networkidle")
            self.step_pass(page, 8, "Click Confirm Order")
        except Exception as e:
            self.step_fail(page, 8, f"Checkout step failed: {e}")
            return "Fail", f"Checkout failed at a step: {e}"

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["Thank you", "Your order", "order number", "successfully placed"]), \
            "Order success message not found"
        self.step_pass(page, 9, "Verify order success page with confirmation message")

        return "Pass", "Order placed successfully. Confirmation page displayed."
