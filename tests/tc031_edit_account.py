"""TC-031: Edit Account Information"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC031_EditAccount(BaseTest):
    TC_ID    = "TC-031"
    SUMMARY  = "Edit Account Information"
    MODULE   = "My Account"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-031","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-031","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(BASE_URL + "customer/info", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to My Account info page")

        d = D.all_tc("TC-031")
        page.locator("#FirstName").fill(d.get("new_first_name","SmokeTest"))
        self.step_pass(page, 3, "Update First Name to 'SmokeTest'")

        page.locator("input[value='Save'], button:has-text('Save')").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 4, "Click Save button")

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["successfully", "saved", "updated", "The customer info"]), \
            "Success message not found after save"
        self.step_pass(page, 5, "Verify success message after saving account info")

        return "Pass", "Account information updated and saved successfully."
