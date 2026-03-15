"""TC-033: View Order History"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC033_OrderHistory(BaseTest):
    TC_ID    = "TC-033"
    SUMMARY  = "View Order History"
    MODULE   = "My Account"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-033","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-033","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(BASE_URL + "customer/orders", wait_until="domcontentloaded")
        self.step_pass(page, 2, "Navigate to Order History page")

        assert "orders" in page.url.lower(), "Not on orders page"
        self.step_pass(page, 3, "Verify Order History page loaded")

        orders_section = page.locator(".order-list, .orders-table, .customer-orders")
        expect(orders_section.first).to_be_visible(timeout=8_000)
        self.step_pass(page, 4, "Verify orders section visible on page")

        return "Pass", "Order History page loaded successfully."
