"""TC-029: Complete Order Placement"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC029_PlaceOrder(BaseTest):
    TC_ID    = "TC-029"
    SUMMARY  = "Complete Order Placement"
    MODULE   = "Checkout Process"
    PRIORITY = "Critical"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")
        d    = D.all_tc(self.TC_ID)

        page.goto(base + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(d.get("email", D.config("admin_email")))
        page.locator("#Password").fill(d.get("password", D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(base + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.locator("input[value='Add to cart'], button:has-text('Add to cart')").first.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 2, "Add product to cart")

        page.goto(base + "cart")
        page.locator("button:has-text('Checkout'), input[value='Checkout']").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Proceed to Checkout")

        try:
            page.wait_for_selector(
                "input[id*='FirstName'], input[name*='FirstName']",
                timeout=8_000
            )
            page.locator("input[id*='FirstName'], input[name*='FirstName']").first.fill(d.get("billing_fname","Smoke"))
            page.locator("input[id*='LastName'], input[name*='LastName']").first.fill(d.get("billing_lname","Tester"))
            email_fields = page.locator("input[id*='Email'], input[name*='Email']")
            (email_fields.nth(1) if email_fields.count() > 1 else email_fields.first).fill(d.get("billing_email","smoke@test.com"))
            page.locator("select[id*='Country'], select[name*='Country']").first.select_option(label=d.get("billing_country","United States"))
            page.wait_for_timeout(500)
            page.locator("input[id*='City'], input[name*='City']").first.fill(d.get("billing_city","New York"))
            page.locator("input[id*='Address1'], input[name*='Address1']").first.fill(d.get("billing_address","123 Test St"))
            page.locator("input[id*='Zip'], input[id*='Postal'], input[name*='Zip']").first.fill(d.get("billing_zip","10001"))
            page.locator("input[id*='Phone'], input[name*='Phone']").first.fill(d.get("billing_phone","1234567890"))
            page.locator("input[onclick*='Billing.save'], .new-address-next-step-button, button:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
            self.step_pass(page, 4, "Fill billing address and continue")

            page.locator("input[onclick*='Shipping.save'], .shipping-method-next-step-button, button:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
            self.step_pass(page, 5, "Select shipping and continue")

            page.locator("input[onclick*='PaymentMethod.save'], .payment-method-next-step-button, button:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
            self.step_pass(page, 6, "Select payment method and continue")

            page.locator("input[onclick*='PaymentInfo.save'], .payment-info-next-step-button, button:has-text('Continue')").first.click()
            page.wait_for_timeout(2000)
            self.step_pass(page, 7, "Confirm payment info and continue")

            page.locator("input[onclick*='Confirm.save'], button:has-text('Confirm'), input[value='Confirm']").first.click()
            page.wait_for_load_state("networkidle")
            self.step_pass(page, 8, "Click Confirm Order")

        except Exception as ex:
            self.step_fail(page, 8, f"Checkout step failed: {str(ex)[:80]}")
            return "Fail", f"Checkout failed: {str(ex)[:150]}"

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["Thank you", "Your order", "order number", "successfully placed"]), \
            "Order success message not found"
        self.step_pass(page, 9, "Verify order confirmation page shown")

        return "Pass", "Order placed successfully. Confirmation displayed."

if __name__ == "__main__":
    r = TC029_PlaceOrder().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
