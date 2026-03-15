"""TC-010: Register with Invalid Email Format"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC010_RegisterInvalidEmail(BaseTest):
    TC_ID    = "TC-010"
    SUMMARY  = "Register with Invalid Email Format"
    MODULE   = "User Registration"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "register", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Register page")

        page.locator("#FirstName").fill("Test")
        page.locator("#LastName").fill("User")
        d = D.all_tc("TC-010")
        page.locator("#Email").fill(d.get("invalid_email","invalidemail"))
        page.locator("#Password").fill("Test@1234")
        page.locator("#ConfirmPassword").fill("Test@1234")
        self.step_pass(page, 2, "Fill form with invalid email 'invalidemail'")

        page.locator("#register-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Click Register button")

        body = page.locator("body").inner_text()
        assert any(p in body for p in [d.get("expected_message","valid email"), "Wrong email", "Please enter"]), \
            "Expected invalid email error not shown"
        self.step_pass(page, 4, "Verify invalid email format error displayed")

        return "Pass", "Correct validation error shown for invalid email format."
