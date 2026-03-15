"""
utils/base_test.py
───────────────────
Base class for all test cases.
- Does NOT write to the JIRA import sheet (kept clean for manual use)
- Generates: HTML report + Excel result file (with screenshots per step)
"""

from __future__ import annotations
import time
import traceback
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path
import sys

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.config import (BROWSER, HEADLESS, SLOW_MO, VIEWPORT_W,
                           VIEWPORT_H, PAGE_TIMEOUT, TESTER_NAME, RETRY_COUNT)
from utils.screenshot_manager import ScreenshotManager


class BaseTest(ABC):

    TC_ID:    str = ""
    SUMMARY:  str = ""
    MODULE:   str = ""
    PRIORITY: str = "High"

    def __init__(self):
        self.sm:     ScreenshotManager | None = None
        self._steps: list[dict] = []
        self.result: dict       = {}

    @abstractmethod
    def execute(self, page: Page) -> tuple[str, str]:
        """Implement test steps. Return (status, actual_result)."""

    # ── Step helpers – ONE screenshot each ───────────────────────────────────
    def step_pass(self, page: Page, number: int, name: str, notes: str = "") -> None:
        self._capture(page, number, name, status="pass", notes=notes)

    def step_fail(self, page: Page, number: int, name: str, notes: str = "") -> None:
        self._capture(page, number, name, status="fail", notes=notes)

    def _capture(self, page: Page, number: int, name: str,
                 status: str, notes: str) -> None:
        ts   = datetime.now().strftime("%H:%M:%S")
        icon = "✅" if status == "pass" else "❌"
        print(f"  {icon}  [{ts}] Step {number}: {name}"
              + (f" – {notes}" if notes else ""))
        path = self.sm.capture(page, number, name, status=status, notes=notes)
        self._steps.append({
            "number":          number,
            "name":            name,
            "status":          status,
            "notes":           notes,
            "timestamp":       ts,
            "screenshot_path": str(path),
        })

    # ── Runner ────────────────────────────────────────────────────────────────
    def run(self) -> dict:
        status        = "Fail"
        actual_result = ""
        defect_id     = ""
        comments      = ""
        start_time    = time.time()

        for attempt in range(1, RETRY_COUNT + 2):
            self._steps = []
            self.sm     = ScreenshotManager(self.TC_ID)

            print(f"\n{'='*65}")
            print(f"  {self.TC_ID} | {self.SUMMARY}"
                  + (f"  [Retry {attempt}]" if attempt > 1 else ""))
            print(f"{'='*65}")

            with sync_playwright() as pw:
                browser_type = getattr(pw, BROWSER)
                browser: Browser = browser_type.launch(
                    headless=HEADLESS,
                    slow_mo=SLOW_MO,
                    args=["--no-sandbox", "--disable-setuid-sandbox"]
                )
                context: BrowserContext = browser.new_context(
                    viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
                )
                context.set_default_timeout(PAGE_TIMEOUT)
                page = context.new_page()

                console_errors: list[str] = []
                page.on("console", lambda m: console_errors.append(m.text)
                        if m.type == "error" else None)

                try:
                    status, actual_result = self.execute(page)
                    if console_errors:
                        comments = "Console errors: " + "; ".join(console_errors[:3])
                    break

                except AssertionError as ae:
                    status        = "Fail"
                    actual_result = f"Assertion failed: {ae}"
                    comments      = str(ae)
                    self.step_fail(page, 99, "Assertion Error", notes=str(ae))
                    print(f"  ❌  FAIL – {ae}")
                    if attempt > RETRY_COUNT:
                        break

                except Exception as ex:
                    status        = "Fail"
                    actual_result = f"Unexpected error: {ex}"
                    comments      = traceback.format_exc()[:400]
                    self.step_fail(page, 99, "Unexpected Error", notes=str(ex))
                    print(f"  ❌  ERROR – {ex}")
                    if attempt > RETRY_COUNT:
                        break

                finally:
                    context.close()
                    browser.close()

        elapsed   = time.time() - start_time
        exec_time = f"{int(elapsed//60):02d}:{int(elapsed%60):02d}"
        exec_date = datetime.now().strftime("%Y-%m-%d")

        print(f"\n  {'✅' if status=='Pass' else '❌'}  {self.TC_ID} → {status}"
              f"  ({exec_time})  |  {len(self._steps)} screenshot(s)")

        self.result = {
            "tc_id":         self.TC_ID,
            "summary":       self.SUMMARY,
            "module":        self.MODULE,
            "priority":      self.PRIORITY,
            "status":        status,
            "actual_result": actual_result,
            "exec_date":     exec_date,
            "exec_time":     exec_time,
            "tester":        TESTER_NAME,
            "defect_id":     defect_id,
            "comments":      comments,
            "steps":         self._steps,
        }
        return self.result
