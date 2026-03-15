"""TC-007: Register with Valid Details"""
from __future__ import annotations
from pathlib import Path, os
import sys, time
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC007_RegisterValid(BaseTest):
    TC_ID    = "TC-007"
    SUMMARY  = "Register with Valid Details"
    MODULE   = "User Registration"
    PRIORITY = "Critical"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to home page")

        page.locator("a:has-text('Register')").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Click Register link")

        ts = str(int(time.time()))
        d = D.all_tc("TC-007")
        email = f'{d.get("email_prefix","smoketest")}_{ts}@{d.get("email_domain","testmail.com")}'
        page.locator("#FirstName").fill(d.get("first_name","Smoke"))
        page.locator("#LastName").fill(d.get("last_name","Tester"))
        self.step_pass(page, 3, "Fill First Name and Last Name")

        page.locator("#Email").fill(email)
        self.step_pass(page, 4, f"Fill Email – {email}")

        page.locator("#Password").fill(d.get("password","Test@1234"))
        page.locator("#ConfirmPassword").fill(d.get("password","Test@1234"))
        self.step_pass(page, 5, "Fill Password and Confirm Password")

        page.locator("#register-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 6, "Click Register button")

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["Your registration completed", "successfully", "continue"]), \
            "Registration success message not found"
        self.step_pass(page, 7, "Verify registration success message displayed")

        return "Pass", f"Registration successful with email: {email}"
