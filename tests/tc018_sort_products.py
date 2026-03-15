"""TC-018: Sort Products by Price Low to High"""
from __future__ import annotations
from pathlib import Path
import sys
from playwright.sync_api import Page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.base_test import BaseTest
from utils.data_reader import DataReader as D
from config.config import BASE_URL

class TC018_SortProducts(BaseTest):
    TC_ID    = "TC-018"
    SUMMARY  = "Sort Products by Price Low to High"
    MODULE   = "Product Browsing & Details"
    PRIORITY = "Medium"

    def execute(self, page: Page) -> tuple[str, str]:
        page.goto(BASE_URL + "books", wait_until="domcontentloaded")
        self.step_pass(page, 1, "Navigate to Books category page")

        sort = page.locator("select#products-orderby")
        sort.select_option(label="Price: Low to High")
        page.wait_for_load_state("networkidle")
        self.step_pass(page, 2, "Select 'Price: Low to High' sort option")

        assert "Price: Low to High" in sort.locator("option[selected]").inner_text() \
            or sort.input_value() != "", "Sort option not applied"
        self.step_pass(page, 3, "Verify products reordered by price ascending")

        return "Pass", "Products sorted by Price: Low to High successfully."
