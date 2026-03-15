"""TC-008: Register with Existing Email"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC008_RegisterExistingEmail(BaseTest):
    TC_ID    = "TC-008"
    SUMMARY  = "Register with Existing Email"
    MODULE   = "User Registration"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "register", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Register page")

        page.locator("#FirstName").fill("Test")
        page.locator("#LastName").fill("User")
        d = D.all_tc("TC-008")
        page.locator("#Email").fill(d.get("existing_email","admin@yourstore.com"))
        page.locator("#Password").fill(d.get("password","Test@1234"))
        page.locator("#ConfirmPassword").fill("Test@1234")
        self.step_pass(page, 2, "Fill form with already-registered email")

        page.locator("#register-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Click Register button")

        body = page.locator("body").inner_text()
        assert any(p in body for p in [d.get("expected_message","already exists"), "already registered", "The specified email"]), \
            "Expected duplicate email error not shown"
        self.step_pass(page, 4, "Verify duplicate email error message displayed")

        return "Pass", "Correct error shown for already-registered email."
