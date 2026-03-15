"""TC-014: Logout Successfully"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC014_Logout(BaseTest):
    TC_ID    = "TC-014"
    SUMMARY  = "Logout Successfully"
    MODULE   = "User Login & Logout"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        # Login first
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-014","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-014","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login with valid credentials")

        page.locator("a:has-text('Log out')").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Click Log Out link")

        login_link = page.locator("a:has-text('Log in')")
        expect(login_link.first).to_be_visible(timeout=8_000)
        self.step_pass(page, 3, "Verify Log In link visible – logout successful")

        return "Pass", "Logout successful. Log In link visible in header."
