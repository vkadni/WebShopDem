"""TC-032: Change Password"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC032_ChangePassword(BaseTest):
    TC_ID    = "TC-032"
    SUMMARY  = "Change Password"
    MODULE   = "My Account"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-032","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-032","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(BASE_URL + "customer/changepassword", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to Change Password page")

        d = D.all_tc("TC-032")
        page.locator("#OldPassword").fill(d.get("current_password","admin"))
        self.step_pass(page, 3, "Enter current/old password")

        page.locator("#NewPassword").fill(d.get("new_password","Admin@9999"))
        page.locator("#ConfirmNewPassword").fill(d.get("new_password","Admin@9999"))
        self.step_pass(page, 4, "Enter new password and confirm")

        page.locator("input[value='Change password'], button:has-text('Change password')").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 5, "Click Change Password button")

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["Password was changed", "successfully", "changed"]), \
            "Password change success message not found"
        self.step_pass(page, 6, "Verify password changed successfully message")

        # Restore original password
        page.goto(BASE_URL + "customer/changepassword")
        page.locator("#OldPassword").fill(d.get("new_password","Admin@9999"))
        page.locator("#NewPassword").fill(d.get("restore_password","admin"))
        page.locator("#ConfirmNewPassword").fill(d.get("restore_password","admin"))
        page.locator("input[value='Change password'], button:has-text('Change password')").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 7, "Restore original password for subsequent tests")

        return "Pass", "Password changed successfully and restored."
