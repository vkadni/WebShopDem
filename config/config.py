"""
config.py – Central configuration
Reads from ENV variables first, then falls back to test_data.xlsx Config sheet.
This means Jenkins can override any value via ENV without touching Excel.
"""

import os
from pathlib import Path

BASE_DIR       = Path(__file__).resolve().parent.parent
DATA_DIR       = BASE_DIR / "data"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
REPORT_DIR     = BASE_DIR / "reports"

EXCEL_DATA_FILE   = DATA_DIR / "test_data.xlsx"
EXCEL_RESULT_FILE = DATA_DIR / "DemoWebShop_Smoke_Tests_JIRA_Import.xlsx"

def _from_excel(key: str, fallback: str) -> str:
    """Try to read from Config sheet; use fallback if Excel not available."""
    try:
        from utils.data_reader import DataReader
        val = DataReader.config(key)
        return val if val else fallback
    except Exception:
        return fallback

# ── Application ───────────────────────────────────────────────────────────────
BASE_URL = os.getenv("APP_URL") or _from_excel("base_url", "https://demowebshop.tricentis.com/")

# ── Browser ───────────────────────────────────────────────────────────────────
BROWSER      = os.getenv("BROWSER")  or _from_excel("browser",         "chromium")
HEADLESS     = (os.getenv("HEADLESS") or _from_excel("headless",       "false")).lower() == "true"
SLOW_MO      = int(os.getenv("SLOW_MO")  or _from_excel("slow_mo_ms", "500"))
VIEWPORT_W   = int(os.getenv("VIEWPORT_W", "1366"))
VIEWPORT_H   = int(os.getenv("VIEWPORT_H", "768"))
PAGE_TIMEOUT = int(os.getenv("PAGE_TIMEOUT") or _from_excel("page_timeout_ms", "30000"))

# ── Execution ─────────────────────────────────────────────────────────────────
TESTER_NAME  = os.getenv("TESTER_NAME") or _from_excel("tester_name",  "Automation")
RETRY_COUNT  = int(os.getenv("RETRY_COUNT") or _from_excel("retry_count", "1"))
PARALLEL     = os.getenv("PARALLEL", "false").lower() == "true"

# ── Reporting ─────────────────────────────────────────────────────────────────
GENERATE_HTML_REPORT = True
HTML_REPORT_NAME     = "smoke_test_report.html"
