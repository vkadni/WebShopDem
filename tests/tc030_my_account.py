"""TC-030: View My Account Page"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC030_MyAccount(BaseTest):
    TC_ID    = "TC-030"
    SUMMARY  = "View My Account Page"
    MODULE   = "My Account"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")
        page.goto(base + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc(self.TC_ID, "email", D.config("admin_email")))
        page.locator("#Password").fill(D.tc(self.TC_ID, "password", D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(base + "customer/info", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to My Account page")

        # Broader selector for account info form fields
        account_form = page.locator(
            "input[id*='FirstName'], input[name*='FirstName'], "
            "input[id*='first-name'], .customer-info-wrapper, "
            "form[action*='customer']"
        ).first
        expect(account_form).to_be_visible(timeout=8_000)
        self.step_pass(page, 3, "Verify account info form visible")

        nav = page.locator(".block-account-navigation, .account-navigation, .side-2").first
        expect(nav).to_be_visible(timeout=5_000)
        self.step_pass(page, 4, "Verify account navigation menu visible")

        return "Pass", "My Account page loaded with form and navigation."

if __name__ == "__main__":
    r = TC030_MyAccount().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
