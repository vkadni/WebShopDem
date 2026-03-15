"""TC-031: Edit Account Information"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC031_EditAccount(BaseTest):
    TC_ID    = "TC-031"
    SUMMARY  = "Edit Account Information"
    MODULE   = "My Account"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")
        d    = D.all_tc(self.TC_ID)
        page.goto(base + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(d.get("email", D.config("admin_email")))
        page.locator("#Password").fill(d.get("password", D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(base + "customer/info", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to My Account info page")

        fname = page.locator(
            "input[id*='FirstName'], input[name*='FirstName'], input[id*='first-name']"
        ).first
        fname.wait_for(timeout=8_000)
        fname.fill(d.get("new_first_name", "SmokeTest"))
        self.step_pass(page, 3, f"Update First Name to '{d.get('new_first_name','SmokeTest')}'")

        page.locator(
            "input[value='Save'], button:has-text('Save'), "
            "input[type='submit'], .save-customer-info-button"
        ).first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 4, "Click Save button")

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["successfully", "saved", "updated", "customer info"]), \
            "Success message not found after save"
        self.step_pass(page, 5, "Verify success message after saving")

        return "Pass", "Account information updated successfully."

if __name__ == "__main__":
    r = TC031_EditAccount().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
