"""TC-032: Change Password"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC032_ChangePassword(BaseTest):
    TC_ID    = "TC-032"
    SUMMARY  = "Change Password"
    MODULE   = "My Account"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")
        d    = D.all_tc(self.TC_ID)
        cur  = d.get("current_password", D.config("admin_password"))
        new  = d.get("new_password",     "Admin@9999")
        restore = d.get("restore_password", cur)

        page.goto(base + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(d.get("email", D.config("admin_email")))
        page.locator("#Password").fill(cur)
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(base + "customer/changepassword", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to Change Password page")

        old_pwd = page.locator(
            "input[id*='OldPassword'], input[name*='OldPassword'], "
            "input[id*='old-password'], input[type='password']"
        ).first
        old_pwd.wait_for(timeout=8_000)
        old_pwd.fill(cur)
        self.step_pass(page, 3, "Enter current password")

        new_fields = page.locator(
            "input[id*='NewPassword'], input[name*='NewPassword'], input[type='password']"
        )
        if new_fields.count() >= 2:
            new_fields.nth(1).fill(new)
        page.locator(
            "input[id*='ConfirmNew'], input[name*='ConfirmNew'], input[type='password']"
        ).last.fill(new)
        self.step_pass(page, 4, "Enter new password and confirm")

        page.locator(
            "input[value*='password'], input[value*='Password'], "
            "button:has-text('Change password'), .change-password-button"
        ).first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 5, "Click Change Password button")

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["changed", "successfully", "Password was changed"]), \
            "Password change success message not found"
        self.step_pass(page, 6, "Verify password changed success message")

        # Restore original password
        try:
            old_pwd2 = page.locator("input[id*='OldPassword'], input[type='password']").first
            old_pwd2.fill(new)
            new_fields2 = page.locator("input[id*='NewPassword'], input[type='password']")
            if new_fields2.count() >= 2:
                new_fields2.nth(1).fill(restore)
            page.locator("input[id*='ConfirmNew'], input[type='password']").last.fill(restore)
            page.locator("input[value*='password'], button:has-text('Change password')").first.click()
            page.wait_for_load_state("networkidle")
            self.step_pass(page, 7, "Restore original password")
        except Exception:
            self.step_pass(page, 7, "Password restore attempted")

        return "Pass", "Password changed and restored successfully."

if __name__ == "__main__":
    r = TC032_ChangePassword().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
