"""
Report tools — generate_pdf, generate_json.
Generates appraisal reports from structured data.
"""
import os
import json
from datetime import datetime


REPORTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "reports"
)


def generate_json(report_data: dict, faculty_id: str, run_id: str) -> dict:
    """Generate a JSON appraisal report."""
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        filename = f"appraisal_{faculty_id}_{run_id}.json"
        filepath = os.path.join(REPORTS_DIR, filename)

        report = {
            "report_type": "Faculty Appraisal Report",
            "generated_at": datetime.now().isoformat(),
            "status": "DRAFT — Awaiting Human Review",
            "disclaimer": "DEMO Appraisal Policy — configurable; not official institutional scoring policy.",
            **report_data
        }

        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)

        return {"status": "success", "path": filepath, "filename": filename}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _generate_pure_pdf(report_data: dict, faculty_id: str, run_id: str, filepath: str, filename: str) -> dict:
    """Generate a clean, valid PDF in pure Python when fpdf is unavailable."""
    profile = report_data.get("faculty", {})
    scores = report_data.get("scores", {})
    validation = report_data.get("validation_summary", {})
    warnings = report_data.get("warnings", [])
    comparison = report_data.get("comparison", {})

    lines = [
        "Faculty Appraisal Report",
        "DEMO Appraisal Policy - Configurable; not official institutional scoring policy.",
        "Status: DRAFT - Awaiting Human Review",
        "----------------------------------------------------------------------",
        f"Faculty ID: {profile.get('faculty_id', faculty_id)}",
        f"Name: {profile.get('name', 'N/A')}",
        f"Department: {profile.get('department', 'N/A')}",
        f"Designation: {profile.get('designation', 'N/A')}",
        f"Academic Year: {profile.get('academic_year', 'N/A')}",
        "----------------------------------------------------------------------",
        "Appraisal Score Breakdown:",
        f"  Research: {scores.get('research', {}).get('score', 0)} / {scores.get('research', {}).get('max_score', 40)}",
        f"  Teaching: {scores.get('teaching', {}).get('score', 0)} / {scores.get('teaching', {}).get('max_score', 40)}",
        f"  Administration: {scores.get('administration', {}).get('score', 0)} / {scores.get('administration', {}).get('max_score', 20)}",
        f"  Total Score: {scores.get('total_score', 0)} / {scores.get('max_score', 100)}",
        "----------------------------------------------------------------------",
        f"Validation: VALID={validation.get('VALID', 0)}, INVALID={validation.get('INVALID', 0)}, REVIEW={validation.get('NEEDS_REVIEW', 0)}",
    ]

    res_counts = report_data.get("detailed_breakdown", {}).get("research", {}).get("summary_counts", {})
    if res_counts:
        lines.append("----------------------------------------------------------------------")
        lines.append(f"Research Output: Total Papers={res_counts.get('total_papers', 0)} (Journals={res_counts.get('journal_publications', 0)}, Conferences={res_counts.get('conference_proceedings', 0)})")
        lines.append(f"Innovation & Grants: Patents={res_counts.get('patents_granted', 0)}, Projects={res_counts.get('sponsored_projects', 0)}")

    if comparison:
        lines.append(f"Comparison with Previous: Prev={comparison.get('previous_score', 'N/A')}, Diff={comparison.get('difference', 'N/A')}")
    if warnings:
        lines.append(f"Warnings ({len(warnings)}): " + "; ".join(str(w) for w in warnings[:3]))
    lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Run: {run_id}")

    content_stream = "BT\n/F1 11 Tf\n40 780 Td\n15 TL\n"
    for line in lines:
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        content_stream += f"({escaped}) '\n"
    content_stream += "ET\n"
    stream_bytes = content_stream.encode("latin1")

    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    obj3 = b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
    obj4 = b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    obj5 = b"5 0 obj\n<< /Length " + str(len(stream_bytes)).encode("ascii") + b" >>\nstream\n" + stream_bytes + b"endstream\nendobj\n"

    header = b"%PDF-1.4\n"
    pos1 = len(header)
    pos2 = pos1 + len(obj1)
    pos3 = pos2 + len(obj2)
    pos4 = pos3 + len(obj3)
    pos5 = pos4 + len(obj4)
    xref_pos = pos5 + len(obj5)

    xref = (
        f"xref\n0 6\n"
        f"0000000000 65535 f \n"
        f"{pos1:010d} 00000 n \n"
        f"{pos2:010d} 00000 n \n"
        f"{pos3:010d} 00000 n \n"
        f"{pos4:010d} 00000 n \n"
        f"{pos5:010d} 00000 n \n"
        f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n"
    ).encode("ascii")

    pdf_bytes = header + obj1 + obj2 + obj3 + obj4 + obj5 + xref
    with open(filepath, "wb") as f:
        f.write(pdf_bytes)

    return {"status": "success", "path": filepath, "filename": filename}


def generate_pdf(report_data: dict, faculty_id: str, run_id: str) -> dict:
    """Generate a PDF appraisal report using fpdf2 (or pure-python fallback)."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filename = f"appraisal_{faculty_id}_{run_id}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)

    try:
        from fpdf import FPDF
    except (ImportError, ModuleNotFoundError):
        return _generate_pure_pdf(report_data, faculty_id, run_id, filepath, filename)

    try:

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Faculty Appraisal Report", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 6, "DEMO Appraisal Policy - configurable; not official institutional scoring policy.", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(5)

        # Status banner
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(255, 243, 205)
        pdf.cell(0, 8, f"Status: DRAFT - Awaiting Human Review", new_x="LMARGIN", new_y="NEXT", fill=True, align="C")
        pdf.ln(5)

        # Faculty Info
        profile = report_data.get("faculty", {})
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Faculty Information", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        for key in ["faculty_id", "name", "department", "designation", "academic_year"]:
            val = profile.get(key, "N/A")
            pdf.cell(50, 6, f"{key.replace('_', ' ').title()}:", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 6, str(val), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        # Scores
        scores = report_data.get("scores", {})
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Appraisal Score Breakdown", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)

        for cat in ["research", "teaching", "administration"]:
            cat_data = scores.get(cat, {})
            s = cat_data.get("score", 0)
            m = cat_data.get("max_score", 0)
            pdf.cell(60, 6, f"{cat.title()}:", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 6, f"{s} / {m}", new_x="LMARGIN", new_y="NEXT")

        total = scores.get("total_score", 0)
        max_total = scores.get("max_score", 100)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(60, 8, "Total:", new_x="RIGHT", new_y="TOP")
        pdf.cell(0, 8, f"{total} / {max_total}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        # Scholarship & Output Breakdown
        res_counts = report_data.get("detailed_breakdown", {}).get("research", {}).get("summary_counts", {})
        if res_counts:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 7, "Research & Scholarship Output", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(70, 6, "Total Research Papers:", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 6, f"{res_counts.get('total_papers', 0)} (Journals: {res_counts.get('journal_publications', 0)}, Conferences: {res_counts.get('conference_proceedings', 0)})", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(70, 6, "Patents Granted / Filed:", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 6, str(res_counts.get('patents_granted', 0)), new_x="LMARGIN", new_y="NEXT")
            pdf.cell(70, 6, "Sponsored R&D Projects:", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 6, str(res_counts.get('sponsored_projects', 0)), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

        # Validation Summary
        validation = report_data.get("validation_summary", {})
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Evidence Validation Summary", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        for status_key in ["VALID", "INVALID", "NEEDS_REVIEW"]:
            count = validation.get(status_key, 0)
            pdf.cell(60, 6, f"{status_key}:", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 6, str(count), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        # Warnings
        warnings = report_data.get("warnings", [])
        if warnings:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "Warnings", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            for w in warnings:
                pdf.cell(5, 6, "-", new_x="RIGHT", new_y="TOP")
                pdf.cell(0, 6, str(w), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

        # Comparison with previous
        comparison = report_data.get("comparison", {})
        if comparison:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "Comparison with Previous Appraisal", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 10)
            prev = comparison.get("previous_score", "N/A")
            curr = comparison.get("current_score", "N/A")
            diff = comparison.get("difference", "N/A")
            pdf.cell(60, 6, "Previous Score:", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 6, str(prev), new_x="LMARGIN", new_y="NEXT")
            pdf.cell(60, 6, "Current Score:", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 6, str(curr), new_x="LMARGIN", new_y="NEXT")
            pdf.cell(60, 6, "Difference:", new_x="RIGHT", new_y="TOP")
            pdf.cell(0, 6, str(diff), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

        # Footer
        pdf.set_font("Helvetica", "I", 8)
        pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, f"Run ID: {run_id}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 6, "This is an educational prototype using synthetic data.", new_x="LMARGIN", new_y="NEXT")

        pdf.output(filepath)
        return {"status": "success", "path": filepath, "filename": filename}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# Tool registry entry
TOOLS = {
    "generate_pdf": {
        "function": generate_pdf,
        "description": "Generate PDF appraisal report",
        "inputs": ["report_data", "faculty_id", "run_id"],
    },
    "generate_json": {
        "function": generate_json,
        "description": "Generate JSON appraisal report",
        "inputs": ["report_data", "faculty_id", "run_id"],
    },
}
