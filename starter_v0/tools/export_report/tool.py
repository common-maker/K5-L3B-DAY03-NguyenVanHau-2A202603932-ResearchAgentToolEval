from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from tools._shared import ROOT


def export_report(
    filename: str = "",
    content: str = "",
    overwrite: bool = True,
) -> dict[str, Any]:
    """Saves a research digest or report to a local markdown or text file."""
    if not filename or not filename.strip():
        return {
            "tool": "export_report",
            "filename": "",
            "path": "",
            "bytes_written": 0,
            "status": "error",
            "error": "filename is required",
        }

    if not content or not content.strip():
        return {
            "tool": "export_report",
            "filename": filename,
            "path": "",
            "bytes_written": 0,
            "status": "error",
            "error": "content is required",
        }

    # Sanitize filename: take only basename to prevent directory traversal
    safe_name = os.path.basename(filename.strip())
    if not safe_name.endswith((".md", ".txt", ".markdown", ".json")):
        safe_name += ".md"

    # Save under artifacts/reports/
    reports_dir = ROOT / "artifacts" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    target_path = reports_dir / safe_name

    if target_path.exists() and not overwrite:
        return {
            "tool": "export_report",
            "filename": safe_name,
            "path": str(target_path),
            "bytes_written": 0,
            "status": "skipped",
            "message": f"File {safe_name} already exists and overwrite is False",
        }

    try:
        data = content.encode("utf-8")
        target_path.write_bytes(data)
        return {
            "tool": "export_report",
            "filename": safe_name,
            "path": str(target_path),
            "bytes_written": len(data),
            "status": "saved",
        }
    except Exception as exc:
        return {
            "tool": "export_report",
            "filename": safe_name,
            "path": str(target_path),
            "bytes_written": 0,
            "status": "error",
            "error": str(exc),
        }
