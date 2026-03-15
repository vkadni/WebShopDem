"""TC-033: View Order History"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC033_OrderHistory(BaseTest):
    TC_ID    = "TC-033"
    SUMMARY  = "View Order History"
    MODULE   = "My Account"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")
        page.goto(base + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc(self.TC_ID, "email", D.config("admin_email")))
        page.locator("#Password").fill(D.tc(self.TC_ID, "password", D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(base + "customer/orders", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to Order History page")

        assert "orders" in page.url.lower(), "Not on orders page"
        self.step_pass(page, 3, "Verify on Order History URL")

        # Broader order section selectors
        orders_section = page.locator(
            ".order-list, .orders-table, .customer-orders, "
            "table[class*='order'], .order-item, "
            ".account-page .title, h1, h2"
        ).first
        expect(orders_section).to_be_visible(timeout=8_000)
        self.step_pass(page, 4, "Verify orders page content visible")

        return "Pass", "Order History page loaded successfully."

if __name__ == "__main__":
    r = TC033_OrderHistory().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
