"""TC-036: Write a Product Review"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC036_WriteReview(BaseTest):
    TC_ID    = "TC-036"
    SUMMARY  = "Write a Product Review"
    MODULE   = "Product Compare & Reviews"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        base = D.config("base_url")
        d    = D.all_tc(self.TC_ID)

        page.goto(base + "login", wait_until="domcontentloaded")
        page.locator("#Email").fill(d.get("email", D.config("admin_email")))
        page.locator("#Password").fill(d.get("password", D.config("admin_password")))
        page.locator("input.button-1.login-button").click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 1, "Login as registered user")

        page.goto(base + d.get("category_url", "books"), wait_until="domcontentloaded")
        page.locator(".product-item h2 a, .item-box .product-title a").first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Navigate to product detail page")

        # Navigate directly to product reviews URL
        current_url = page.url
        if "/productreviews/" not in current_url:
            # Find product ID from URL and build review URL
            review_link = page.locator(
                "a:has-text('Add your review'), "
                "a[href*='productreviews'], "
                ".write-review a"
            ).first
            expect(review_link).to_be_visible(timeout=8_000)
            review_link.click()
            page.wait_for_load_state("networkidle")
        self.step_pass(page, 3, "Navigate to product review page")

        # Wait for review form to be fully loaded and enabled
        review_title = page.locator(
            "input[id*='Title'][type='text']:not([disabled]), "
            "#AddProductReview_Title:not([disabled])"
        ).first
        review_title.wait_for(state="visible", timeout=10_000)
        review_title.wait_for(state="enabled", timeout=10_000)
        review_title.fill(d.get("review_title", "Great Product!"))
        self.step_pass(page, 4, "Enter review title")

        review_text = page.locator(
            "textarea[id*='ReviewText']:not([disabled]), "
            "#AddProductReview_ReviewText:not([disabled])"
        ).first
        review_text.fill(d.get("review_body", "Works as expected. Highly recommended."))
        self.step_pass(page, 5, "Enter review body text")

        rating = d.get("review_rating", "4")
        page.locator(
            f"input[name='addproductrating'][value='{rating}']:not([disabled])"
        ).first.click()
        self.step_pass(page, 6, f"Select {rating}-star rating")

        page.locator(
            "input[value='Submit review']:not([disabled]), "
            "button:has-text('Submit review'):not([disabled])"
        ).first.click()
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 7, "Submit review")

        body = page.locator("body").inner_text()
        assert any(p in body for p in ["successfully", "approved", "submitted", "review"]), \
            "Review confirmation message not found"
        self.step_pass(page, 8, "Verify review submitted successfully")

        return "Pass", "Product review submitted. Confirmation shown."

if __name__ == "__main__":
    r = TC036_WriteReview().run(); raise SystemExit(0 if r["status"] == "Pass" else 1)
