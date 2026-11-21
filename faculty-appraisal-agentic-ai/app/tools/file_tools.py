"""
File tools — read_file, read_pdf, read_csv, read_xlsx.
All file reads are auditable tool calls used by agents.
"""
import os
import csv
import json

# Safe directory boundary for evidence files
BASE_DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "faculty"
)


def _resolve_safe_path(relative_path: str, faculty_id: str) -> str:
    """Resolve a file path within the safe data directory. Rejects path traversal."""
    base = os.path.join(BASE_DATA_DIR, faculty_id)
    full = os.path.normpath(os.path.join(base, relative_path))
    if not full.startswith(os.path.normpath(base)):
        raise PermissionError(f"Access denied: path '{relative_path}' is outside allowed directory for {faculty_id}")
    return full


def read_file(file_path: str, faculty_id: str) -> dict:
    """
    Read a text file within the faculty data directory.
    Returns: {"status": "success", "content": ..., "path": ...} or error dict.
    """
    try:
        safe_path = _resolve_safe_path(file_path, faculty_id)
        if not os.path.exists(safe_path):
            return {"status": "error", "error": f"File not found: {file_path}", "path": file_path}
        with open(safe_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return {"status": "success", "content": content, "path": file_path, "size": len(content)}
    except PermissionError as e:
        return {"status": "rejected", "error": str(e), "path": file_path}
    except Exception as e:
        return {"status": "error", "error": str(e), "path": file_path}


def read_pdf(file_path: str, faculty_id: str) -> dict:
    """
    Read a PDF file. For this educational prototype, we read the file as text.
    Real implementation would use a PDF parser; here evidence PDFs are text-based placeholders.
    """
    try:
        safe_path = _resolve_safe_path(file_path, faculty_id)
        if not os.path.exists(safe_path):
            return {"status": "error", "error": f"PDF not found: {file_path}", "path": file_path}
        with open(safe_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return {"status": "success", "content": content, "path": file_path, "format": "pdf"}
    except PermissionError as e:
        return {"status": "rejected", "error": str(e), "path": file_path}
    except Exception as e:
        return {"status": "error", "error": str(e), "path": file_path}


def read_csv(file_path: str, faculty_id: str) -> dict:
    """
    Read a CSV file and return structured data.
    Returns: {"status": "success", "rows": [...], "columns": [...]} or error dict.
    """
    try:
        safe_path = _resolve_safe_path(file_path, faculty_id)
        if not os.path.exists(safe_path):
            return {"status": "error", "error": f"CSV not found: {file_path}", "path": file_path}
        with open(safe_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [dict(row) for row in reader]
            columns = reader.fieldnames or []
        return {"status": "success", "rows": rows, "columns": columns, "row_count": len(rows), "path": file_path}
    except PermissionError as e:
        return {"status": "rejected", "error": str(e), "path": file_path}
    except Exception as e:
        return {"status": "error", "error": str(e), "path": file_path}


def read_xlsx(file_path: str, faculty_id: str) -> dict:
    """
    Read an XLSX file and return structured data.
    """
    try:
        safe_path = _resolve_safe_path(file_path, faculty_id)
        if not os.path.exists(safe_path):
            return {"status": "error", "error": f"XLSX not found: {file_path}", "path": file_path}
        import pandas as pd
        df = pd.read_excel(safe_path)
        rows = df.to_dict(orient="records")
        columns = list(df.columns)
        return {"status": "success", "rows": rows, "columns": columns, "row_count": len(rows), "path": file_path}
    except PermissionError as e:
        return {"status": "rejected", "error": str(e), "path": file_path}
    except Exception as e:
        return {"status": "error", "error": str(e), "path": file_path}


# Tool registry entry for the runtime
TOOLS = {
    "read_file": {
        "function": read_file,
        "description": "Read a text file from faculty evidence directory",
        "inputs": ["file_path", "faculty_id"],
    },
    "read_pdf": {
        "function": read_pdf,
        "description": "Read a PDF evidence file",
        "inputs": ["file_path", "faculty_id"],
    },
    "read_csv": {
        "function": read_csv,
        "description": "Read a CSV data file and return structured rows",
        "inputs": ["file_path", "faculty_id"],
    },
    "read_xlsx": {
        "function": read_xlsx,
        "description": "Read an XLSX data file and return structured rows",
        "inputs": ["file_path", "faculty_id"],
    },
}
