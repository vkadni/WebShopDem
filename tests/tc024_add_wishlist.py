"""TC-024: Add Product to Wishlist"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC024_AddWishlist(BaseTest):
    TC_ID    = "TC-024"
    SUMMARY  = "Add Product to Wishlist"
    MODULE   = "Wishlist"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-024","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-024","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Navigate to a product detail page")

        page.locator("input[value='Add to wishlist'], button:has-text('Add to wishlist')").first.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 3, "Click Add to Wishlist button")

        notif = page.locator(".bar-notification, .success, #bar-notification")
        expect(notif.first).to_be_visible(timeout=8_000)
        self.step_pass(page, 4, "Verify success notification shown for wishlist add")

        return "Pass", "Product added to wishlist. Success notification displayed."
