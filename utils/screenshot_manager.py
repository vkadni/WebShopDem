"""
utils/screenshot_manager.py
────────────────────────────
Captures a full-page screenshot for every test step and maintains
an ordered manifest (used later by the HTML reporter).
"""

from __future__ import annotations
import time
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from playwright.sync_api import Page

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.config import SCREENSHOT_DIR


@dataclass
class StepScreenshot:
    step_number: int
    step_name:   str
    filepath:    Path
    timestamp:   str
    status:      str          # "pass" | "fail" | "info"
    notes:       str = ""


class ScreenshotManager:
    """
    Takes and tracks screenshots for every step in a test case.

    Usage:
        sm = ScreenshotManager("TC-001")
        sm.capture(page, step_number=1, step_name="Navigate to home page")
        sm.capture(page, step_number=2, step_name="Verify logo", status="pass")
        report_data = sm.get_manifest()
    """

    def __init__(self, tc_id: str):
        self.tc_id    = tc_id
        self.run_id   = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.tc_dir   = SCREENSHOT_DIR / tc_id / self.run_id
        self.tc_dir.mkdir(parents=True, exist_ok=True)
        self._steps: list[StepScreenshot] = []

    # ── Public API ────────────────────────────────────────────────────────────
    def capture(
        self,
        page:        Page,
        step_number: int,
        step_name:   str,
        status:      str = "info",   # "pass" | "fail" | "info"
        notes:       str = "",
    ) -> Path:
        """
        Capture a full-page screenshot for the given step.
        Returns the saved file path.
        """
        safe_name = step_name[:50].replace(" ", "_").replace("/", "-")
        filename  = f"step{step_number:02d}_{status.upper()}_{safe_name}.png"
        filepath  = self.tc_dir / filename
        ts        = datetime.now().strftime("%H:%M:%S")

        try:
            page.screenshot(path=str(filepath), full_page=True)
            icon = {"pass": "✅", "fail": "❌", "info": "📸"}.get(status, "📸")
            print(f"    {icon}  [{ts}] Step {step_number} screenshot → {filename}")
        except Exception as ex:
            print(f"    ⚠️  Screenshot failed at step {step_number}: {ex}")

        self._steps.append(StepScreenshot(
            step_number=step_number,
            step_name=step_name,
            filepath=filepath,
            timestamp=ts,
            status=status,
            notes=notes,
        ))
        return filepath

    def capture_fail(self, page: Page, step_number: int, reason: str) -> Path:
        """Convenience method for failure screenshots."""
        return self.capture(page, step_number, f"FAIL_{reason[:40]}", status="fail", notes=reason)

    def get_manifest(self) -> list[StepScreenshot]:
        """Return ordered list of all captured screenshots."""
        return self._steps

    def tc_screenshot_dir(self) -> Path:
        return self.tc_dir

    def summary(self) -> str:
        total = len(self._steps)
        fails = sum(1 for s in self._steps if s.status == "fail")
        return f"{total} screenshots ({fails} failure captures) → {self.tc_dir}"
