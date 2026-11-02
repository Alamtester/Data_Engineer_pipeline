
# import csv
# import html
# from pathlib import Path


# # Project root / reports directory
# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# REPORT_DIR = PROJECT_ROOT / "reports"


# def generate_pipeline_report(report_data):
#     """
#     Generate separate CSV and HTML reports for one pipeline run.

#     Returns the paths created and any reporting errors.
#     Reporting errors do not raise exceptions into main.py.
#     """

#     REPORT_DIR.mkdir(parents=True, exist_ok=True)

#     run_id = report_data["run_id"]
#     csv_path = REPORT_DIR / f"pipeline_report_{run_id}.csv"
#     html_path = REPORT_DIR / f"pipeline_report_{run_id}.html"

#     # These fields appear in both reports.
#     fields = [
#         "run_id",
#         "pipeline_name",
#         "status",
#         "start_time",
#         "end_time",
#         "duration_seconds",
#         "records_extracted",
#         "records_transformed",
#         "records_loaded",
#         "previous_watermark",
#         "new_watermark",
#         "failed_stage",
#         "error_message",
#     ]

#     # Prepare a complete row even if some values are unavailable.
#     row = {field: report_data.get(field, "") for field in fields}

#     created_files = []
#     report_errors = []

#     # 1. Generate CSV report
#     try:
#         with csv_path.open(
#             mode="w",
#             newline="",
#             encoding="utf-8-sig",
#         ) as file:
#             writer = csv.DictWriter(file, fieldnames=fields)
#             writer.writeheader()
#             writer.writerow(row)

#         created_files.append(str(csv_path))

#     except Exception as exc:
#         report_errors.append(f"CSV report failed: {exc}")

#     # 2. Generate HTML report
#     try:
#         status = str(row["status"]).upper()
#         status_color = "#198754" if status == "SUCCESS" else "#dc3545"

#         def safe(value):
#             return html.escape(str(value if value is not None else ""))

#         report_rows = ""
#         for field in fields:
#             report_rows += (
#                 "<tr>"
#                 f"<th>{safe(field.replace('_', ' ').title())}</th>"
#                 f"<td>{safe(row[field])}</td>"
#                 "</tr>"
#             )

#         html_content = f"""<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Customer Data Pipeline Report</title>
#     <style>
#         body {{
#             font-family: Arial, sans-serif;
#             max-width: 1000px;
#             margin: 35px auto;
#             padding: 0 20px;
#             color: #212529;
#             background: #f8f9fa;
#         }}
#         h1 {{ margin-bottom: 8px; }}
#         .subtitle {{ color: #6c757d; }}
#         .status {{
#             display: inline-block;
#             padding: 8px 14px;
#             border-radius: 6px;
#             background: {status_color};
#             color: white;
#             font-weight: bold;
#         }}
#         .panel {{
#             background: white;
#             border: 1px solid #dee2e6;
#             border-radius: 8px;
#             padding: 20px;
#             margin-top: 20px;
#         }}
#         table {{
#             width: 100%;
#             border-collapse: collapse;
#             overflow-wrap: anywhere;
#         }}
#         th, td {{
#             padding: 11px;
#             text-align: left;
#             border-bottom: 1px solid #dee2e6;
#         }}
#         th {{ width: 35%; background: #f1f3f5; }}
#         .error {{ color: #b02a37; white-space: pre-wrap; }}
#     </style>
# </head>
# <body>
#     <h1>Customer Data Pipeline Report</h1>
#     <p class="subtitle">SQL Server → Python → PostgreSQL</p>
#     <p class="status">{safe(status)}</p>

#     <div class="panel">
#         <h2>Execution Summary</h2>
#         <p><strong>Pipeline:</strong> {safe(row["pipeline_name"])}</p>
#         <p><strong>Run ID:</strong> {safe(row["run_id"])}</p>
#         <p><strong>Duration:</strong>
#            {safe(row["duration_seconds"])} seconds</p>
#         <p><strong>Records extracted:</strong>
#            {safe(row["records_extracted"])}</p>
#         <p><strong>Records transformed:</strong>
#            {safe(row["records_transformed"])}</p>
#         <p><strong>Records loaded:</strong>
#            {safe(row["records_loaded"])}</p>
#     </div>

#     <div class="panel">
#         <h2>Execution Details</h2>
#         <table>
#             <tbody>
#                 {report_rows}
#             </tbody>
#         </table>
#     </div>

#     <p class="error">{safe(row["error_message"])}</p>
# </body>
# </html>
# """

#         html_path.write_text(html_content, encoding="utf-8")
#         created_files.append(str(html_path))

#     except Exception as exc:
#         report_errors.append(f"HTML report failed: {exc}")

#     return {
#         "created_files": created_files,
#         "errors": report_errors,
#     }




import csv
import html
import json
import re
from pathlib import Path
from datetime import datetime


REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"

REPORT_FIELDS = [
    "run_id",
    "pipeline_name",
    "status",
    "start_time",
    "end_time",
    "duration_seconds",
    "records_extracted",
    "records_transformed",
    "records_loaded",
    "previous_watermark",
    "new_watermark",
    "failed_stage",
    "error_message",
]


def safe_value(value):
    """Convert values into safe, readable strings."""
    return "" if value is None else str(value)


def format_number(value):
    try:
        return f"{int(value or 0):,}"
    except (ValueError, TypeError):
        return "0"


def build_interactive_html(report_data):
    """Build a standalone, interactive HTML pipeline dashboard."""

    data = {
        field: safe_value(report_data.get(field))
        for field in REPORT_FIELDS
    }

    status = data["status"].upper()
    is_success = status in {"SUCCESS", "SUCCESSFUL", "COMPLETED"}

    status_class = "success" if is_success else "failed"
    status_label = "SUCCESS" if is_success else "FAILED"

    extracted = int(report_data.get("records_extracted") or 0)
    transformed = int(report_data.get("records_transformed") or 0)
    loaded = int(report_data.get("records_loaded") or 0)

    def percentage(value, total):
        if total <= 0:
            return 0
        return min(100, max(0, round(value / total * 100)))

    transform_percent = percentage(transformed, extracted)
    load_percent = percentage(loaded, transformed)

    def esc(value):
        return html.escape(safe_value(value))

    # Escape JSON so report values cannot break the script element.
    json_data = json.dumps(report_data, default=str)
    json_data = (
        json_data.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )

    template = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pipeline Monitoring Dashboard</title>

<style>
:root {
    --bg: #f3f6fb;
    --card: #ffffff;
    --text: #172033;
    --muted: #65718a;
    --border: #e3e8f0;
    --accent: #4169e1;
    --track: #e9edf5;
}
body.dark {
    --bg: #111827;
    --card: #1f2937;
    --text: #f3f4f6;
    --muted: #aab4c5;
    --border: #374151;
    --accent: #93aaff;
    --track: #374151;
}
* { box-sizing: border-box; }
body {
    margin: 0;
    padding: 28px;
    background: var(--bg);
    color: var(--text);
    font-family: Inter, "Segoe UI", Arial, sans-serif;
    transition: background .2s, color .2s;
}
.container { max-width: 1200px; margin: auto; }
header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}
h1 { margin: 0 0 6px; font-size: 28px; }
h2 { font-size: 18px; margin-top: 0; }
.subtitle { color: var(--muted); font-size: 14px; }
.actions { display: flex; gap: 8px; flex-wrap: wrap; }
button {
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--text);
    padding: 10px 14px;
    border-radius: 9px;
    cursor: pointer;
    font-weight: 600;
}
button:hover { border-color: var(--accent); }
.status-banner {
    padding: 18px 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 5px solid var(--accent);
}
.status-banner.success { border-left-color: #16a34a; }
.status-banner.failed { border-left-color: #dc2626; }
.badge {
    display: inline-block;
    border-radius: 999px;
    padding: 7px 12px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .5px;
}
.badge.success { color: #15803d; background: #dcfce7; }
.badge.failed { color: #b91c1c; background: #fee2e2; }
.grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 20px;
}
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    min-width: 0;
}
.metric-label { color: var(--muted); font-size: 13px; }
.metric-value { font-size: 28px; font-weight: 750; margin-top: 10px; }
.metric-note { color: var(--muted); font-size: 12px; margin-top: 8px; }
.two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 20px;
}
.progress-row { margin: 18px 0; }
.progress-title {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    font-size: 13px;
    margin-bottom: 8px;
}
.track {
    height: 10px;
    border-radius: 99px;
    background: var(--track);
    overflow: hidden;
}
.bar {
    height: 100%;
    border-radius: 99px;
    background: var(--accent);
    transition: width .4s;
}
.details {
    display: grid;
    grid-template-columns: minmax(120px, 180px) 1fr;
    gap: 0;
}
.detail-label, .detail-value {
    padding: 11px 0;
    border-bottom: 1px solid var(--border);
    overflow-wrap: anywhere;
    font-size: 13px;
}
.detail-label { color: var(--muted); padding-right: 12px; }
.detail-value { font-weight: 500; }
.error-box {
    background: #fff1f2;
    color: #9f1239;
    padding: 14px;
    border-radius: 9px;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    font: 13px/1.6 Consolas, monospace;
}
body.dark .error-box { background: #3b1f2a; color: #fecdd3; }
.error-stage { margin-bottom: 12px; font-weight: 700; }
.muted { color: var(--muted); font-size: 13px; }
footer {
    color: var(--muted);
    text-align: center;
    padding: 22px 0 4px;
    font-size: 12px;
}
@media (max-width: 850px) {
    .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .two-columns { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
    body { padding: 14px; }
    h1 { font-size: 23px; }
    .grid { grid-template-columns: 1fr 1fr; gap: 10px; }
    .card { padding: 14px; }
    .metric-value { font-size: 23px; }
    .details { grid-template-columns: 1fr; }
    .detail-label { border-bottom: 0; padding-bottom: 3px; }
    .detail-value { padding-top: 3px; }
}
@media print {
    body { padding: 0; background: white; color: black; }
    .actions { display: none; }
    .card, .status-banner { break-inside: avoid; }
}
</style>
</head>

<body>
<div class="container">

<header>
    <div>
        <h1>Data Pipeline Dashboard</h1>
        <div class="subtitle">SQL Server → Python → PostgreSQL</div>
        <div class="subtitle">Run ID: __RUN_ID__</div>
    </div>
    <div class="actions">
        <button onclick="toggleTheme()">◐ Dark mode</button>
        <button onclick="copySummary()">Copy summary</button>
        <button onclick="downloadJSON()">Download JSON</button>
        <button onclick="window.print()">Print report</button>
    </div>
</header>

<section class="status-banner __STATUS_CLASS__">
    <div>
        <strong>Pipeline: __PIPELINE_NAME__</strong>
        <div class="subtitle">Started: __START_TIME__</div>
    </div>
    <span class="badge __STATUS_CLASS__">● __STATUS_LABEL__</span>
</section>

<section class="grid">
    <div class="card">
        <div class="metric-label">Execution duration</div>
        <div class="metric-value">__DURATION__ s</div>
        <div class="metric-note">Total reported run time</div>
    </div>
    <div class="card">
        <div class="metric-label">Records extracted</div>
        <div class="metric-value">__EXTRACTED__</div>
        <div class="metric-note">Read from SQL Server</div>
    </div>
    <div class="card">
        <div class="metric-label">Records transformed</div>
        <div class="metric-value">__TRANSFORMED__</div>
        <div class="metric-note">Processed by Python</div>
    </div>
    <div class="card">
        <div class="metric-label">Records loaded</div>
        <div class="metric-value">__LOADED__</div>
        <div class="metric-note">Sent to PostgreSQL</div>
    </div>
</section>

<section class="two-columns">
    <div class="card">
        <h2>Processing overview</h2>

        <div class="progress-row">
            <div class="progress-title">
                <span>Extraction</span><strong>__EXTRACTED__ records</strong>
            </div>
            <div class="track"><div class="bar" style="width:100%"></div></div>
        </div>

        <div class="progress-row">
            <div class="progress-title">
                <span>Transformation / extraction</span>
                <strong>__TRANSFORM_PERCENT__%</strong>
            </div>
            <div class="track"><div class="bar" style="width:__TRANSFORM_PERCENT__%"></div></div>
        </div>

        <div class="progress-row">
            <div class="progress-title">
                <span>Loading / transformation</span>
                <strong>__LOAD_PERCENT__%</strong>
            </div>
            <div class="track"><div class="bar" style="width:__LOAD_PERCENT__%"></div></div>
        </div>

        <p class="muted">These percentages compare reported record counts; they are not a measure of data quality.</p>
    </div>

    <div class="card">
        <h2>Run information</h2>
        <div class="details">
            <div class="detail-label">Pipeline name</div><div class="detail-value">__PIPELINE_NAME__</div>
            <div class="detail-label">Run ID</div><div class="detail-value">__RUN_ID__</div>
            <div class="detail-label">Start time</div><div class="detail-value">__START_TIME__</div>
            <div class="detail-label">End time</div><div class="detail-value">__END_TIME__</div>
            <div class="detail-label">Final status</div><div class="detail-value">__STATUS_LABEL__</div>
        </div>
    </div>
</section>

<section class="card" style="margin-bottom:20px">
    <h2>Incremental load watermarks</h2>
    <div class="details">
        <div class="detail-label">Previous watermark</div><div class="detail-value">__PREVIOUS_WATERMARK__</div>
        <div class="detail-label">New watermark</div><div class="detail-value">__NEW_WATERMARK__</div>
    </div>
    <p class="muted">The watermark helps determine which source records to read on a subsequent run.</p>
</section>

<section class="card" style="margin-bottom:20px">
    <h2>Failure details</h2>
    <div id="failureContent">__FAILURE_CONTENT__</div>
</section>

<section class="card">
    <details>
        <summary style="cursor:pointer;font-weight:700">View raw report data</summary>
        <pre id="rawData" style="white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px"></pre>
    </details>
</section>

<footer>Generated by the Python Data Pipeline Reporting Module</footer>
</div>

<script>
const reportData = __REPORT_JSON__;

function toggleTheme() {
    document.body.classList.toggle("dark");
}

async function copySummary() {
    const summary = [
        "Pipeline: " + (reportData.pipeline_name || ""),
        "Status: " + (reportData.status || ""),
        "Run ID: " + (reportData.run_id || ""),
        "Extracted: " + (reportData.records_extracted ?? 0),
        "Transformed: " + (reportData.records_transformed ?? 0),
        "Loaded: " + (reportData.records_loaded ?? 0),
        "Duration: " + (reportData.duration_seconds ?? 0) + " seconds",
        "Failed stage: " + (reportData.failed_stage || "None"),
        "Error: " + (reportData.error_message || "None")
    ].join("\n");

    try {
        await navigator.clipboard.writeText(summary);
        alert("Pipeline summary copied.");
    } catch (error) {
        window.prompt("Copy this pipeline summary:", summary);
    }
}

function downloadJSON() {
    const blob = new Blob(
        [JSON.stringify(reportData, null, 2)],
        { type: "application/json" }
    );
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "pipeline_report_" +
        String(reportData.run_id || "run").replace(/[^a-zA-Z0-9_-]/g, "_") +
        ".json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
}

document.getElementById("rawData").textContent =
    JSON.stringify(reportData, null, 2);
</script>
</body>
</html>
"""

    failed_stage = data["failed_stage"]
    error_message = data["error_message"]

    if failed_stage or error_message:
        failure_content = (
            f'<div class="error-stage">Stage: {esc(failed_stage or "Unknown")}</div>'
            f'<div class="error-box">{esc(error_message or "No error message provided.")}</div>'
        )
    elif is_success:
        failure_content = (
            '<p style="color:#16a34a;font-weight:600">'
            '✓ No pipeline failure was reported for this run.</p>'
        )
    else:
        failure_content = (
            '<p class="muted">The run failed, but no failure details were recorded.</p>'
        )

    replacements = {
        "__RUN_ID__": esc(data["run_id"]),
        "__PIPELINE_NAME__": esc(data["pipeline_name"]),
        "__STATUS_CLASS__": status_class,
        "__STATUS_LABEL__": status_label,
        "__START_TIME__": esc(data["start_time"]),
        "__END_TIME__": esc(data["end_time"]),
        "__DURATION__": esc(data["duration_seconds"] or "0"),
        "__EXTRACTED__": format_number(extracted),
        "__TRANSFORMED__": format_number(transformed),
        "__LOADED__": format_number(loaded),
        "__TRANSFORM_PERCENT__": str(transform_percent),
        "__LOAD_PERCENT__": str(load_percent),
        "__PREVIOUS_WATERMARK__": esc(data["previous_watermark"] or "Not available"),
        "__NEW_WATERMARK__": esc(data["new_watermark"] or "Not available"),
        "__FAILURE_CONTENT__": failure_content,
        "__REPORT_JSON__": json_data,
    }

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    return template


def generate_pipeline_report(report_data):
    """Generate CSV and interactive HTML reports for a pipeline run."""

    result = {"created_files": [], "errors": []}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    raw_run_id = safe_value(
        report_data.get("run_id") or datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    run_id = re.sub(r"[^a-zA-Z0-9_-]", "_", raw_run_id)

    # Generate CSV report
    csv_path = REPORT_DIR / f"pipeline_report_{run_id}.csv"

    try:
        with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=REPORT_FIELDS)
            writer.writeheader()
            writer.writerow({
                field: safe_value(report_data.get(field))
                for field in REPORT_FIELDS
            })

        result["created_files"].append(str(csv_path))
        print(f"CSV report generated: {csv_path}")

    except Exception as exc:
        message = f"CSV report generation failed: {exc}"
        result["errors"].append(message)
        print(message)

    # Generate interactive HTML report
    html_path = REPORT_DIR / f"pipeline_report_{run_id}.html"

    try:
        html_content = build_interactive_html(report_data)
        html_path.write_text(html_content, encoding="utf-8")

        result["created_files"].append(str(html_path))
        print(f"Interactive HTML report generated: {html_path}")

    except Exception as exc:
        message = f"HTML report generation failed: {exc}"
        result["errors"].append(message)
        print(message)

    return result

