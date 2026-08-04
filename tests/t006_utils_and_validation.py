"""
AUTHOR: Rohan Joseph
PURPOSE: Test the shared token-key, indicator-conversion, and first-value helpers, plus the
         validation guards for required columns and missing files.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-08-04
MODIFIED BY: Rohan Joseph
"""



# ============================================================
# Importing Libraries and Utilities
# ============================================================

import os
import sys
import pytest
import subprocess

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import settings, validation
from src.logger import capture_script_console_to_markdown
from src.utils import (
    compact_path_token,
    convert_indicator_columns_to_int,
    first_non_empty_value,
    normalize_token_key,
)



# ============================================================
# Tests
# ============================================================

def test_normalize_token_key_strips_spaces_and_punctuation():
    """
    Check that the token key strips spaces and punctuation while folding an ampersand.
    This is the join key that aligns column dictionaries and abbreviation maps.
    """

    assert normalize_token_key("Health & Fitness") == "HealthandFitness"
    assert compact_path_token("User ID") == "UserID"


def test_convert_indicator_columns_to_int_clips_to_binary():
    """
    Check that indicator columns coerce to integers and clip to the 0/1 range.
    This keeps disclosure counts stable regardless of raw formatting.
    """

    df = pd.DataFrame({"ind": ["1", "0", "5", ""]})

    converted = convert_indicator_columns_to_int(df, ["ind"])

    assert converted["ind"].tolist() == [1, 0, 1, 0]


def test_first_non_empty_value_skips_blanks():
    """
    Check that the first non-empty, cleaned value is returned from a series.
    This picks a representative value when collapsing repeated app rows.
    """

    assert first_non_empty_value(pd.Series(["", "  ", "Gamma"])) == "Gamma"


def test_require_columns_raises_on_missing():
    """
    Check that require_columns raises a ValidationError when a required column is absent.
    This makes a stage stop early on a malformed source sample.
    """

    frame = pd.DataFrame({"app_id": ["a1"]})

    with pytest.raises(validation.ValidationError):
        validation.require_columns(frame, ["app_id", "Platform"], context = "iOS sample")


def test_require_existing_file_raises_on_missing():
    """
    Check that require_existing_file raises when the path does not exist.
    This turns a missing sample into an actionable error before a stage reads it.
    """

    missing_file = os.path.join(settings.INPUT_DIR, "does_not_exist.csv")

    with pytest.raises(validation.ValidationError):
        validation.require_existing_file(missing_file, context = "app metadata")



# ============================================================
# Main Execution
# ============================================================

def main():
    """
    Run this test module through pytest in a subprocess and echo its output.
    This logs the test run like a pipeline script without the tee fighting pytest's capture.
    """

    command = [sys.executable, "-m", "pytest", __file__, "-v"]
    result = subprocess.run(command, capture_output = True, text = True)

    print(result.stdout, end = "")
    print(result.stderr, end = "")


if __name__ == "__main__":
    capture_script_console_to_markdown(
        run_callable = main,
        script_name = "t006_utils_and_validation",
        log_dir = settings.LOG_DIR,
    )
