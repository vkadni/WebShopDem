"""TC-030: View My Account Page"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC030_MyAccount(BaseTest):
    TC_ID    = "TC-030"
    SUMMARY  = "View My Account Page"
    MODULE   = "My Account"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-030","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-030","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(BASE_URL + "customer/info", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to My Account page")

        first_name = page.locator("#FirstName")
        expect(first_name).to_be_visible(timeout=8_000)
        self.step_pass(page, 3, "Verify account info form visible (FirstName field)")

        nav = page.locator(".block-account-navigation, .account-navigation")
        expect(nav.first).to_be_visible(timeout=5_000)
        self.step_pass(page, 4, "Verify account navigation menu visible")

        return "Pass", "My Account page loaded with profile info and navigation."
