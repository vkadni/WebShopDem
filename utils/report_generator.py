"""
utils/report_generator.py
──────────────────────────
Generates a self-contained HTML report with:
  • Summary stats + pass rate bar
  • Per-TC section with step-by-step table
  • Screenshot embedded inline per step (base64)
  • No external dependencies – single HTML file
"""

from __future__ import annotations
import base64
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config.config import REPORT_DIR

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _b64(path: Path) -> str:
    try:
        return base64.b64encode(path.read_bytes()).decode()
    except Exception:
        return ""


def _badge(status: str) -> str:
    colors = {
        "Pass":        ("#155724","#D4EDDA"),
        "Fail":        ("#721C24","#F8D7DA"),
        "Blocked":     ("#383D41","#E2E3E5"),
        "Not Run":     ("#856404","#FFF3CD"),
        "In Progress": ("#004085","#CCE5FF"),
        "pass":        ("#155724","#D4EDDA"),
        "fail":        ("#721C24","#F8D7DA"),
    }
    fg, bg = colors.get(status, ("#333","#eee"))
    return (f'<span style="background:{bg};color:{fg};padding:2px 10px;'
            f'border-radius:10px;font-weight:700;font-size:11px;'
            f'text-transform:uppercase">{status}</span>')


def generate_html_report(results: list[dict]) -> Path:
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total    = len(results)
    passed   = sum(1 for r in results if r["status"] == "Pass")
    failed   = sum(1 for r in results if r["status"] == "Fail")
    not_run  = sum(1 for r in results if r["status"] == "Not Run")
    blocked  = sum(1 for r in results if r["status"] == "Blocked")
    pct      = round(passed / total * 100, 1) if total else 0

    # ── Summary table rows ────────────────────────────────────────────────────
    sum_rows = ""
    for r in results:
        sum_rows += f"""<tr>
          <td style="font-weight:700;color:#1E4D8C">{r['tc_id']}</td>
          <td>{r['summary']}</td>
          <td>{r['module']}</td>
          <td>{r['priority']}</td>
          <td>{_badge(r['status'])}</td>
          <td>{r.get('exec_date','')}</td>
          <td>{r.get('exec_time','')}</td>
          <td>{r.get('tester','')}</td>
          <td style="color:#721C24;font-weight:600">{r.get('defect_id','') or '—'}</td>
        </tr>"""

    # ── Per-TC detail sections ────────────────────────────────────────────────
    tc_html = ""
    for r in results:
        # Step rows with screenshot
        step_rows = ""
        for s in r.get("steps", []):
            ss_path = Path(s.get("screenshot_path", ""))
            img_tag = ""
            if ss_path.exists():
                b64 = _b64(ss_path)
                if b64:
                    img_tag = (f'<img src="data:image/png;base64,{b64}" '
                               f'style="max-width:480px;width:100%;border-radius:6px;'
                               f'border:1px solid #dee2e6;margin-top:6px;" />')
            else:
                img_tag = '<span style="color:#aaa;font-size:11px">No screenshot</span>'

            s_bg = "#f0fff4" if s["status"] == "pass" else "#fff5f5" if s["status"] == "fail" else "#f8f9fa"
            s_bd = "#c3e6cb" if s["status"] == "pass" else "#f5c6cb" if s["status"] == "fail" else "#dee2e6"

            step_rows += f"""<tr style="background:{s_bg}">
              <td style="text-align:center;font-weight:700;color:#1E4D8C;
                         vertical-align:top;padding-top:10px">{s['number']}</td>
              <td style="vertical-align:top;padding-top:10px">
                <div style="font-weight:600;font-size:13px">{s['name']}</div>
                {"<div style='color:#666;font-size:11px;margin-top:3px'>"+s['notes']+"</div>" if s.get('notes') else ""}
              </td>
              <td style="text-align:center;vertical-align:top;padding-top:10px">
                {_badge(s['status'])}
                <div style="color:#888;font-size:11px;margin-top:4px">{s.get('timestamp','')}</div>
              </td>
              <td style="vertical-align:top;padding:8px">{img_tag}</td>
            </tr>"""

        if not step_rows:
            step_rows = '<tr><td colspan="4" style="color:#aaa;text-align:center;padding:20px">No steps recorded</td></tr>'

        tc_html += f"""
        <div style="border:1px solid #dee2e6;border-radius:10px;margin-bottom:28px;
                    overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
          <!-- TC Header -->
          <div style="background:#1E4D8C;padding:14px 20px;display:flex;
                      justify-content:space-between;align-items:center;">
            <span style="color:white;font-weight:700;font-size:15px">
              {r['tc_id']} &nbsp;–&nbsp; {r['summary']}
            </span>
            {_badge(r['status'])}
          </div>

          <!-- TC Metadata -->
          <div style="background:#f0f4fa;padding:12px 20px;display:grid;
                      grid-template-columns:repeat(4,1fr);gap:8px;font-size:12px;">
            <div><span style="color:#555;font-weight:600">Module:</span> {r['module']}</div>
            <div><span style="color:#555;font-weight:600">Priority:</span> {r['priority']}</div>
            <div><span style="color:#555;font-weight:600">Date:</span> {r.get('exec_date','')}</div>
            <div><span style="color:#555;font-weight:600">Time:</span> {r.get('exec_time','')}</div>
            <div><span style="color:#555;font-weight:600">Tester:</span> {r.get('tester','')}</div>
            <div><span style="color:#555;font-weight:600">Defect:</span>
              <span style="color:#721C24;font-weight:600">{r.get('defect_id','') or '—'}</span></div>
            <div style="grid-column:span 2"><span style="color:#555;font-weight:600">Actual:</span> {r.get('actual_result','')}</div>
          </div>

          <!-- Steps Table -->
          <div style="padding:16px 20px;">
            <div style="font-weight:700;color:#1E4D8C;font-size:13px;
                        border-bottom:2px solid #1E4D8C;padding-bottom:6px;margin-bottom:12px;">
               Step-by-Step Execution with Screenshots
            </div>
            <table style="width:100%;border-collapse:collapse;font-size:13px;">
              <thead>
                <tr style="background:#2E6DA4;">
                  <th style="color:white;padding:8px 12px;width:50px;text-align:center">Step</th>
                  <th style="color:white;padding:8px 12px;text-align:left">Description</th>
                  <th style="color:white;padding:8px 12px;width:110px;text-align:center">Status</th>
                  <th style="color:white;padding:8px 12px;text-align:left">Screenshot</th>
                </tr>
              </thead>
              <tbody>{step_rows}</tbody>
            </table>
          </div>
        </div>"""

    # ── Full page ─────────────────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Test Execution Report – DemoWebShop</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:Arial,sans-serif;background:#f0f2f5;color:#222;font-size:14px}}
  .wrap{{max-width:1300px;margin:0 auto;padding:24px}}
  table{{width:100%;border-collapse:collapse}}
  th{{background:#1E4D8C;color:white;padding:9px 12px;text-align:left;font-size:12px}}
  td{{padding:8px 12px;border-bottom:1px solid #e9ecef;font-size:12px;vertical-align:middle}}
  tr:hover td{{background:#f0f4fb}}
  .card{{background:white;border-radius:10px;padding:20px 24px;
         margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
</style>
</head>
<body>
<div class="wrap">

  <!-- Header banner -->
  <div style="background:linear-gradient(135deg,#1E4D8C,#2E6DA4);color:white;
              border-radius:12px;padding:28px 32px;margin-bottom:22px">
    <div style="font-size:22px;font-weight:900"> Test Execution Report</div>
    <div style="font-size:12px;margin-top:6px;opacity:.85">
      https://demowebshop.tricentis.com/ &nbsp;|&nbsp; Generated: {run_time}
    </div>
  </div>

  <!-- Stats cards -->
  <div class="card">
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:16px;text-align:center">
      <div><div style="font-size:36px;font-weight:900;color:#1E4D8C">{total}</div>
           <div style="font-size:11px;color:#666">Total</div></div>
      <div><div style="font-size:36px;font-weight:900;color:#155724">{passed}</div>
           <div style="font-size:11px;color:#666">Pass</div></div>
      <div><div style="font-size:36px;font-weight:900;color:#721C24">{failed}</div>
           <div style="font-size:11px;color:#666">Fail</div></div>
      <div><div style="font-size:36px;font-weight:900;color:#856404">{not_run}</div>
           <div style="font-size:11px;color:#666">Not Run</div></div>
      <div><div style="font-size:36px;font-weight:900;color:#383D41">{blocked}</div>
           <div style="font-size:11px;color:#666">Blocked</div></div>
      <div><div style="font-size:36px;font-weight:900;color:#155724">{pct}%</div>
           <div style="font-size:11px;color:#666">Pass Rate</div></div>
    </div>
    <div style="margin-top:16px;background:#e9ecef;border-radius:6px;height:8px">
      <div style="background:#28a745;height:100%;width:{pct}%;border-radius:6px"></div>
    </div>
  </div>

  <!-- Summary table -->
  <div class="card">
    <div style="font-size:16px;font-weight:700;color:#1E4D8C;margin-bottom:14px">
       Execution Summary
    </div>
    <table>
      <thead><tr>
        <th>TC ID</th><th>Summary</th><th>Module</th><th>Priority</th>
        <th>Status</th><th>Date</th><th>Time</th><th>Tester</th><th>Defect</th>
      </tr></thead>
      <tbody>{sum_rows}</tbody>
    </table>
  </div>

  <!-- TC detail sections -->
  <div style="font-size:16px;font-weight:700;color:#1E4D8C;margin-bottom:14px">
     Detailed Results &amp; Screenshots
  </div>
  {tc_html}

  <div style="text-align:center;color:#aaa;font-size:11px;padding:20px 0">
    DemoWebShop Automation Framework &nbsp;|&nbsp; {run_time}
  </div>
</div>
</body>
</html>"""

    run_id   = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = REPORT_DIR / f"TestReport_{run_id}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"    HTML report  → {out_path}")
    return out_path
