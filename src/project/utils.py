"""
AUTHOR: Rohan Joseph
PURPOSE: Shared utility functions for formatting, normalization, and diagnostics.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os
import re


import pandas as pd



"""
Functions
"""

def print_section_header(label: str) -> None:
    """
    Print a lightweight section header within a stage run.
    This helps separate report-level or file-level work in the console transcript.
    """

    print(f"\n{label}")


def print_status(message: str) -> None:
    """
    Print a consistently indented status line.
    This helps make logs easier to scan without repeating formatting boilerplate.
    """

    print(f"  > {message}")


def print_stage_banner(label: str) -> None:
    """
    Print a standardized banner for a pipeline stage.
    This helps make run logs easier to scan.
    """

    print("\n" + "-" * 76)
    print(label)
    print("-" * 76 + "\n")


def ensure_parent_dir(file_path: str) -> None:
    """
    Ensure that a file's parent directory exists before writing.
    This helps avoid repeated parent-directory creation code in export steps.
    """

    os.makedirs(os.path.dirname(file_path), exist_ok = True)


def normalize_whitespace(text: str) -> str:
    """
    Normalize repeated whitespace and non-breaking spaces in text.
    This helps stabilize downstream matching and summary output.
    """

    if not isinstance(text, str):
        return ""

    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_token_key(text: str) -> str:
    """
    Normalize a token-like key by removing spaces and punctuation noise.
    This helps robust joins across column dictionaries and abbreviation maps.
    """

    text = normalize_whitespace(text)
    text = text.replace("’", "'")
    text = text.replace("'", "")
    text = text.replace("-", "")
    text = text.replace(",", "")
    text = text.replace("&", "and")
    text = text.replace("/", "")
    text = text.replace(" ", "")
    text = text.replace(".", "")
    return text.strip()


def compact_path_token(text: str) -> str:
    """
    Compact a path segment into the style used by disclosure indicator columns.
    This helps reproducing the iOS and Android wide-column naming conventions.
    """

    return normalize_token_key(text)


def first_non_empty_value(series: pd.Series) -> str:
    """
    Return the first non-empty string-like value from a series.
    This helps deduplicating repeated app-level rows.
    """

    for value in series.tolist():
        if pd.notna(value):
            cleaned_value = normalize_whitespace(str(value))
            if cleaned_value != "":
                return cleaned_value

    return ""


def convert_indicator_columns_to_int(dataframe: pd.DataFrame, indicator_columns: list[str]) -> pd.DataFrame:
    """
    Convert indicator columns to deterministic integer flags.
    This helps stable aggregation and summary-statistics generation.
    """

    prepared_dataframe = dataframe.copy()

    if indicator_columns:
        prepared_dataframe[indicator_columns] = (
            prepared_dataframe[indicator_columns]
            .apply(pd.to_numeric, errors = "coerce")
            .fillna(0)
            .clip(lower = 0, upper = 1)
            .astype(int)
        )

    return prepared_dataframe


def build_positive_column_string(row: pd.Series, indicator_columns: list[str]) -> str:
    """
    Convert the active indicator columns for a row into a stable pipe-delimited string.
    This helps compact inspection of wide disclosure outputs.
    """

    positive_columns = [column for column in indicator_columns if int(row.get(column, 0)) == 1]
    return " | ".join(positive_columns)
