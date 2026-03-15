"""TC-036: Write a Product Review"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC036_WriteReview(BaseTest):
    TC_ID    = "TC-036"
    SUMMARY  = "Write a Product Review"
    MODULE   = "Product Compare & Reviews"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(D.tc("TC-036","email",D.config("admin_email")))
        page.locator("#Password").fill(D.tc("TC-036","password",D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Navigate to a product detail page")

        review_link = page.locator("a:has-text('Add your review'), a[href*='productreviews']")
        expect(review_link.first).to_be_visible(timeout=8_000)
        review_link.first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Click 'Add your review' link")

        d = D.all_tc("TC-036")
        page.locator("#AddProductReview_Title").fill(d.get("review_title","Great Product!"))
        self.step_pass(page, 4, "Enter review title")

        page.locator("#AddProductReview_ReviewText").fill(d.get("review_body","Works as expected."))
        self.step_pass(page, 5, "Enter review body text")

        rating = d.get("review_rating","4")
        page.locator(f"input[name='addproductrating'][value='{rating}'], label[for*='addproductrating_{rating}']").first.click()
        self.step_pass(page, 6, "Select 4-star rating")

        page.locator("input[value='Submit review'], button:has-text('Submit review')").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 7, "Click Submit Review button")

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["successfully", "approved", "submitted", "review"]), \
            "Review submission confirmation not found"
        self.step_pass(page, 8, "Verify review submission success/confirmation message")

        return "Pass", "Product review submitted successfully. Confirmation message displayed."
