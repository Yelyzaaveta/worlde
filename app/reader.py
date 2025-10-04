"""Module for reading sentences from Excel files."""

from pathlib import Path

import pandas as pd
from result import Err, Ok, Result


def read_sentences(
    excel_file: Path,
    sheet_name: str | None = None,
) -> Result[list[str], str]:
    """
    Read sentences from an Excel file.

    Args:
        excel_file: Path to the Excel file
        sheet_name: Name of the sheet to read. If None, tries first sheet or 'data' sheet

    Returns:
        Result containing list of sentences as strings or error message
    """
    if not excel_file.exists():
        return Err(f"File not found: {excel_file}")

    df = None

    if sheet_name:
        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        except Exception as e:
            return Err(f"Could not read sheet '{sheet_name}': {e}")
    else:
        # Try first sheet by index
        try:
            df = pd.read_excel(excel_file, sheet_name=0, header=None)
        except Exception:
            # Try 'data' sheet
            try:
                df = pd.read_excel(excel_file, sheet_name="data", header=None)
            except Exception as e:
                return Err(
                    f"Could not read the first sheet or 'data' sheet. "
                    f"Please specify the sheet name explicitly: {e}"
                )

    # Assume single column with sentences
    df.columns = ["sentence"]
    sentences = df["sentence"].fillna("").astype(str).tolist()

    return Ok(sentences)
