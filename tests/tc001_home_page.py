"""TC-001: Verify Home Page Loads"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page, expect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D

class TC001_HomePageLoads(BaseTest):
    TC_ID    = "TC-001"
    SUMMARY  = "Verify Home Page Loads"
    MODULE   = "Home Page & Navigation"
    PRIORITY = "High"

    def execute(self, page: Page) -> tuple[str, str]:
        d = D.all_tc(self.TC_ID)
        url            = d.get("url",            D.config("base_url"))
        expected_title = d.get("expected_title", "Demo Web Shop")
        nav_items      = [x.strip() for x in d.get("nav_items", "Books,Computers,Electronics,Apparel").split(",")]

        page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        page.wait_for_load_state("networkidle", timeout=15_000)
        self.step_pass(page, 1, "Navigate to DemoWebShop home page", notes=f"URL: {page.url}")

        title = page.title()
        assert expected_title in title, f"Title mismatch: '{title}'"
        self.step_pass(page, 2, f"Verify page title – '{title}'")

        expect(page.locator("div.header-logo, .logo, img[alt*='logo']").first).to_be_visible(timeout=8_000)
        self.step_pass(page, 3, "Verify site logo is visible")

        for item in nav_items:
            expect(page.locator(f"ul.top-menu a:has-text('{item}'), .top-menu a:has-text('{item}')").first).to_be_visible(timeout=5_000)
        self.step_pass(page, 4, f"Verify top nav links – {', '.join(nav_items)}")

        count = page.locator(".product-item, .item-box").count()
        assert count > 0, "No featured products found"
        self.step_pass(page, 5, f"Verify featured products – {count} product(s) visible")

        search = page.locator("input#small-searchterms, input[name='q'], .search-box input").first
        expect(search).to_be_visible(timeout=5_000)
        expect(search).to_be_enabled()
        self.step_pass(page, 6, "Verify search bar visible and enabled")

        expect(page.locator("a:has-text('Register')").first).to_be_visible(timeout=5_000)
        expect(page.locator("a:has-text('Log in')").first).to_be_visible(timeout=5_000)
        self.step_pass(page, 7, "Verify Register and Log In links in header")

        expect(page.locator("footer, .footer").first).to_be_visible(timeout=5_000)
        self.step_pass(page, 8, "Verify page footer present")

        return "Pass", f"Home page loaded. Title='{title}'. {count} products. All elements verified."

if __name__ == "__main__":
    r = TC001_HomePageLoads().run(); raise SystemExit(0 if r["status"]=="Pass" else 1)
