# DemoWebShop – Playwright Automation Framework

## Features
- ✅ Test data driven from Excel (reads TC data, writes results back)
- 📸 Per-step screenshots (full-page, auto-named, timestamped)
- 🏗️ CI/CD ready – Jenkins pipeline with parameterised builds
- 📄 Self-contained HTML report (screenshots embedded as base64)
- 🔁 Auto-retry on failure (configurable)
- 🌐 Multi-browser support (Chromium / Firefox / WebKit)

---

## Project Structure

```
demowebshop_framework/
│
├── config/
│   └── config.py               # All settings; overridable via ENV vars
│
├── utils/
│   ├── base_test.py            # Abstract base class (browser, steps, timing)
│   ├── excel_manager.py        # Read test data + write results to Excel
│   ├── screenshot_manager.py   # Per-step screenshot capture & manifest
│   └── report_generator.py     # Self-contained HTML report generator
│
├── tests/
│   └── tc001_home_page.py      # TC-001 implementation (add more here)
│
├── data/
│   └── DemoWebShop_Smoke_Tests_JIRA_Import.xlsx   # ← place your Excel here
│
├── screenshots/                # Auto-created; organised by TC/run
├── reports/                    # Auto-created; HTML report output
│
├── jenkins/
│   └── Jenkinsfile             # Declarative Jenkins pipeline
│
├── run_tests.py                # Main suite runner (CLI entry point)
└── requirements.txt
```

---

## Quick Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Place your Excel file in:
data/DemoWebShop_Smoke_Tests_JIRA_Import.xlsx

# 3. Run TC-001
python tests/tc001_home_page.py

# 4. Run full suite
python run_tests.py

# 5. Run specific TCs
python run_tests.py --tc TC-001

# 6. Run headless (CI mode)
python run_tests.py --headless --browser chromium
```

---

## Output Per Run

| Output | Location |
|--------|----------|
| Screenshots (per step) | `screenshots/TC-001/YYYYMMDD_HHMMSS/` |
| HTML Report | `reports/smoke_test_report.html` |
| Excel Results (J–P) | `data/DemoWebShop_Smoke_Tests_JIRA_Import.xlsx` |

---

## Configuration (config/config.py)

| Variable | Default | ENV Override |
|----------|---------|-------------|
| BASE_URL | https://demowebshop.tricentis.com/ | `APP_URL` |
| BROWSER | chromium | `BROWSER` |
| HEADLESS | true | `HEADLESS` |
| TESTER_NAME | Automation | `TESTER_NAME` |
| RETRY_COUNT | 1 | `RETRY_COUNT` |
| PAGE_TIMEOUT | 30000 ms | `PAGE_TIMEOUT` |

---

## Adding a New Test Case

1. Create `tests/tc00X_your_test.py`
2. Inherit from `BaseTest`
3. Set `TC_ID` and `SUMMARY`
4. Implement the `execute(page)` method using `self.step_pass()` / `self.step_fail()`
5. Register in `run_tests.py → TC_REGISTRY`

```python
from utils.base_test import BaseTest
from playwright.sync_api import Page

class TC002_NavigationLinks(BaseTest):
    TC_ID   = "TC-002"
    SUMMARY = "Verify Top Navigation Category Links"

    def execute(self, page: Page) -> tuple[str, str]:
        self.step(page, 1, "Navigate to home page", status="info")
        page.goto("https://demowebshop.tricentis.com/")
        self.step_pass(page, 1, "Home page loaded")

        self.step(page, 2, "Click Books link", status="info")
        page.click("text=Books")
        self.step_pass(page, 2, "Books page loaded")

        return "Pass", "All navigation links verified."
```

---

## Jenkins CI/CD Setup

1. Install plugins: **Pipeline**, **HTML Publisher**, **Workspace Cleanup**
2. New Item → Pipeline → "Pipeline script from SCM"
3. Point SCM to your repo; Script Path = `jenkins/Jenkinsfile`
4. Build parameters are pre-defined:
   - **BROWSER** – dropdown (chromium/firefox/webkit)
   - **APP_URL** – target environment URL
   - **TC_IDS** – blank = all, or space-separated e.g. `TC-001 TC-002`
   - **HEADLESS** – always true in CI
   - **RETRY_COUNT** – retries on failure
5. The pipeline publishes the HTML report under **"Smoke Test Report"** in Jenkins

### Docker Agent (recommended for isolated CI)
Uncomment the Docker agent block in `Jenkinsfile` and use:
```
mcr.microsoft.com/playwright/python:v1.44.0-jammy
```
This image has Python + all Playwright browsers pre-installed.

---

## Excel Columns Updated After Execution

| Column | Field | Example |
|--------|-------|---------|
| J | Execution Status | Pass / Fail |
| K | Actual Result | What was observed |
| L | Execution Date | 2026-03-14 |
| M | Execution Time | 01:23 |
| N | Executed By | Automation / Jenkins CI |
| O | Defect ID | DEMO-123 |
| P | Comments / Notes | Console errors etc. |
