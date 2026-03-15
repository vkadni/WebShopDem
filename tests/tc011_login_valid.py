"""TC-011: Login with Valid Credentials"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC011_LoginValid(BaseTest):
    TC_ID    = "TC-011"
    SUMMARY  = "Login with Valid Credentials"
    MODULE   = "User Login & Logout"
    PRIORITY = "Critical"
    EMAIL    = D.config("admin_email") or "admin@yourstore.com"
    PASSWORD = D.config("admin_password") or "admin"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Login page")

        page.locator("#Email").fill(self.EMAIL)
        self.step_pass(page, 2, f"Enter email – {self.EMAIL}")

        page.locator("#Password").fill(self.PASSWORD)
        self.step_pass(page, 3, "Enter password")

        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 4, "Click Log In button")

        account = page.locator(".account, a[href='/customer/info']")
        expect(account.first).to_be_visible(timeout=8_000)
        self.step_pass(page, 5, "Verify user account link visible in header – login successful")

        return "Pass", f"Login successful. Account link visible for {self.EMAIL}."
