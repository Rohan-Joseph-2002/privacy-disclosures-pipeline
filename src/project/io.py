"""
AUTHOR: Rohan Joseph
PURPOSE: Input and output helpers for stage scripts.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""

from __future__ import annotations



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os

import pandas as pd



"""
Functions
"""

def read_csv_dataframe(file_path: str, max_rows: int | None = None) -> pd.DataFrame:
    """
    Read a CSV file with optional row limiting.
    This helps centralize consistent pandas loading behavior.
    """

    dataframe = pd.read_csv(file_path, low_memory = False)

    if max_rows is not None:
        dataframe = dataframe.head(max_rows).copy()

    return dataframe


def read_excel_dataframe(file_path: str, max_rows: int | None = None) -> pd.DataFrame:
    """
    Read an Excel file with optional row limiting.
    This helps local taxonomy and abbreviation reference files.
    """

    dataframe = pd.read_excel(file_path)

    if max_rows is not None:
        dataframe = dataframe.head(max_rows).copy()

    return dataframe


def write_csv_dataframe(dataframe: pd.DataFrame, output_path: str) -> None:
    """
    Write a DataFrame to CSV after ensuring its parent directory exists.
    This helps keep stage export code minimal and consistent.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok = True)
    dataframe.to_csv(output_path, index = False)
