"""TC-025: View Wishlist Page"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC025_ViewWishlist(BaseTest):
    TC_ID    = "TC-025"
    SUMMARY  = "View Wishlist Page"
    MODULE   = "Wishlist"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-025","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-025","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(BASE_URL + "wishlist", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to Wishlist page")

        assert "wishlist" in page.url.lower(), "Not on wishlist page"
        self.step_pass(page, 3, "Verify Wishlist page loaded successfully")

        return "Pass", "Wishlist page loaded successfully."
