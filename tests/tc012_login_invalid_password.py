"""TC-012: Login with Invalid Password"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC012_LoginInvalidPassword(BaseTest):
    TC_ID    = "TC-012"
    SUMMARY  = "Login with Invalid Password"
    MODULE   = "User Login & Logout"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Login page")

        d = D.all_tc("TC-012")
        page.locator("#Email").fill(d.get("email",D.config("admin_email")))
        page.locator("#Password").fill(d.get("wrong_password","WrongPassword999!"))
        self.step_pass(page, 2, "Enter valid email with wrong password")

        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Click Log In button")

        body = page.locator("body").inner_text()
        assert any(p in body for p in [d.get("expected_message","unsuccessful"), "incorrect", "Login was unsuccessful"]), \
            "Expected login failure message not shown"
        self.step_pass(page, 4, "Verify login failure error message displayed")

        return "Pass", "Correct error shown for invalid password."
