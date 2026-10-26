
import csv
import html
from pathlib import Path


# Project root / reports directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"


def generate_pipeline_report(report_data):
    """
    Generate separate CSV and HTML reports for one pipeline run.

    Returns the paths created and any reporting errors.
    Reporting errors do not raise exceptions into main.py.
    """

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    run_id = report_data["run_id"]
    csv_path = REPORT_DIR / f"pipeline_report_{run_id}.csv"
    html_path = REPORT_DIR / f"pipeline_report_{run_id}.html"

    # These fields appear in both reports.
    fields = [
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

    # Prepare a complete row even if some values are unavailable.
    row = {field: report_data.get(field, "") for field in fields}

    created_files = []
    report_errors = []

    # 1. Generate CSV report
    try:
        with csv_path.open(
            mode="w",
            newline="",
            encoding="utf-8-sig",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerow(row)

        created_files.append(str(csv_path))

    except Exception as exc:
        report_errors.append(f"CSV report failed: {exc}")

    # 2. Generate HTML report
    try:
        status = str(row["status"]).upper()
        status_color = "#198754" if status == "SUCCESS" else "#dc3545"

        def safe(value):
            return html.escape(str(value if value is not None else ""))

        report_rows = ""
        for field in fields:
            report_rows += (
                "<tr>"
                f"<th>{safe(field.replace('_', ' ').title())}</th>"
                f"<td>{safe(row[field])}</td>"
                "</tr>"
            )

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Data Pipeline Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 35px auto;
            padding: 0 20px;
            color: #212529;
            background: #f8f9fa;
        }}
        h1 {{ margin-bottom: 8px; }}
        .subtitle {{ color: #6c757d; }}
        .status {{
            display: inline-block;
            padding: 8px 14px;
            border-radius: 6px;
            background: {status_color};
            color: white;
            font-weight: bold;
        }}
        .panel {{
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            overflow-wrap: anywhere;
        }}
        th, td {{
            padding: 11px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{ width: 35%; background: #f1f3f5; }}
        .error {{ color: #b02a37; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <h1>Customer Data Pipeline Report</h1>
    <p class="subtitle">SQL Server → Python → PostgreSQL</p>
    <p class="status">{safe(status)}</p>

    <div class="panel">
        <h2>Execution Summary</h2>
        <p><strong>Pipeline:</strong> {safe(row["pipeline_name"])}</p>
        <p><strong>Run ID:</strong> {safe(row["run_id"])}</p>
        <p><strong>Duration:</strong>
           {safe(row["duration_seconds"])} seconds</p>
        <p><strong>Records extracted:</strong>
           {safe(row["records_extracted"])}</p>
        <p><strong>Records transformed:</strong>
           {safe(row["records_transformed"])}</p>
        <p><strong>Records loaded:</strong>
           {safe(row["records_loaded"])}</p>
    </div>

    <div class="panel">
        <h2>Execution Details</h2>
        <table>
            <tbody>
                {report_rows}
            </tbody>
        </table>
    </div>

    <p class="error">{safe(row["error_message"])}</p>
</body>
</html>
"""

        html_path.write_text(html_content, encoding="utf-8")
        created_files.append(str(html_path))

    except Exception as exc:
        report_errors.append(f"HTML report failed: {exc}")

    return {
        "created_files": created_files,
        "errors": report_errors,
    }
