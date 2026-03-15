"""TC-024: Add Product to Wishlist"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC024_AddWishlist(BaseTest):
    TC_ID    = "TC-024"
    SUMMARY  = "Add Product to Wishlist"
    MODULE   = "Wishlist"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(D.config("base_url") + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc(self.TC_ID, "email", D.config("admin_email")))
        page.locator("#Password").fill(D.tc(self.TC_ID, "password", D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(D.config("base_url") + D.tc(self.TC_ID, "category_url", "books"),
                  wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Navigate to product detail page")

        # Multiple wishlist button selectors
        wishlist_btn = page.locator(
            "input[value='Add to wishlist'], "
            ".add-to-wishlist input, "
            ".add-to-wishlist button, "
            "button:has-text('Add to wishlist'), "
            "input.button-2[value*='wishlist']"
        ).first
        expect(wishlist_btn).to_be_visible(timeout=8_000)
        self.step_pass(page, 3, "Verify Add to wishlist button visible")

        wishlist_btn.click()
        page.wait_for_timeout(2000)
        self.step_pass(page, 4, "Click Add to wishlist button")

        notif = page.locator(".bar-notification, .success, #bar-notification").first
        expect(notif).to_be_visible(timeout=8_000)
        self.step_pass(page, 5, "Verify success notification displayed")

        return "Pass", "Product added to wishlist. Success notification shown."

if __name__ == "__main__":
    r = TC024_AddWishlist().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
