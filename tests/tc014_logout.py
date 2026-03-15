"""TC-014: Logout Successfully"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC014_Logout(BaseTest):
    TC_ID    = "TC-014"
    SUMMARY  = "Logout Successfully"
    MODULE   = "User Login & Logout"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(D.config("base_url") + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc(self.TC_ID, "email", D.config("admin_email")))
        page.locator("#Password").fill(D.tc(self.TC_ID, "password", D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login with valid credentials")

        # Try multiple logout link selectors
        logout = page.locator(
            "a.ico-logout, "
            "a[href='/logout'], "
            "a[href*='logout'], "
            ".header-links a:has-text('Log out'), "
            "a:has-text('Log out')"
        ).first
        expect(logout).to_be_visible(timeout=8_000)
        self.step_pass(page, 2, "Verify Log out link visible in header")

        logout.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Click Log out link")

        login_link = page.locator("a:has-text('Log in'), a.ico-login").first
        expect(login_link).to_be_visible(timeout=8_000)
        self.step_pass(page, 4, "Verify Log in link visible – logout successful")

        return "Pass", "Logout successful. Log in link visible in header."

if __name__ == "__main__":
    r = TC014_Logout().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
