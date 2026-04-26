"""
AUTHOR: Rohan Joseph
PURPOSE: Unit tests for validation helpers.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import pandas as pd
import pytest


# --- Import project-specific utilities and pipeline code ---
from project.validation import require_columns



"""
Functions
"""

def test_require_columns_accepts_expected_schema() -> None:
    """
    Ensure the schema validator accepts a dataframe that contains the requested columns.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    df = pd.DataFrame({"app_id": ["1"], "App_Name": ["Example App"]})

    require_columns(df, ["app_id", "App_Name"], "test dataframe")


def test_require_columns_raises_for_missing_fields() -> None:
    """
    Ensure the schema validator raises a clear error when columns are missing.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    df = pd.DataFrame({"app_id": ["1"]})

    with pytest.raises(ValueError):
        require_columns(df, ["app_id", "App_Name"], "test dataframe")
