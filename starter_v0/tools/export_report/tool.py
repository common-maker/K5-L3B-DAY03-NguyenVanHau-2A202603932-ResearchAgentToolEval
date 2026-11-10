from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from tools._shared import ROOT


def export_report(
    filename: str = "report.md",
    content: str = "",
    overwrite: bool = True,
) -> dict[str, Any]:
    """Saves a research digest or report to a local markdown or text file."""
    if not filename or not filename.strip():
        filename = "report.md"

    raw_name = filename.strip()
    if ".." in Path(raw_name).parts or "/" in raw_name or "\\" in raw_name:
        return {
            "tool": "export_report",
            "filename": raw_name,
            "path": "",
            "bytes_written": 0,
            "status": "error",
            "error": "path traversal or directory separator is not allowed",
        }

    if not content or not content.strip():
        return {
            "tool": "export_report",
            "filename": raw_name,
            "path": "",
            "bytes_written": 0,
            "status": "error",
            "error": "content is required",
        }

    safe_name = os.path.basename(raw_name)
    if not safe_name.endswith((".md", ".txt", ".markdown", ".json")):
        safe_name += ".md"

    cwd = Path.cwd()
    if cwd.resolve() != ROOT.resolve() and cwd.resolve() != ROOT.parent.resolve():
        reports_dir = cwd
    else:
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
