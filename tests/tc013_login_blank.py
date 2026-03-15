"""TC-013: Login with Blank Fields"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC013_LoginBlank(BaseTest):
    TC_ID    = "TC-013"
    SUMMARY  = "Login with Blank Fields"
    MODULE   = "User Login & Logout"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Login page")

        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Click Log In with blank email and password")

        errors = page.locator(".field-validation-error, .validation-summary-errors")
        assert errors.count() > 0, "No validation errors shown"
        self.step_pass(page, 3, "Verify validation errors displayed for blank fields")

        return "Pass", "Validation errors correctly shown for blank login fields."
