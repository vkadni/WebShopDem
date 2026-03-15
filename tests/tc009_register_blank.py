"""TC-009: Register with All Blank Fields"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC009_RegisterBlank(BaseTest):
    TC_ID    = "TC-009"
    SUMMARY  = "Register with All Blank Fields"
    MODULE   = "User Registration"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "register", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Register page")

        page.locator("#register-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Click Register with all fields blank")

        errors = page.locator(".field-validation-error, .validation-summary-errors")
        assert errors.count() > 0, "No validation errors shown for blank form"
        self.step_pass(page, 3, f"Verify validation errors displayed – {errors.count()} error(s) found")

        return "Pass", f"Blank form submission shows {errors.count()} validation error(s)."
