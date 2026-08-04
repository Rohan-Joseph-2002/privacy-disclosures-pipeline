"""
AUTHOR: Rohan Joseph
PURPOSE: Test the iOS disclosure preparation — indicator columns coerced to 0/1, the per-row
         disclosure count, and the metadata-match flag from the app metadata merge.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-08-04
MODIFIED BY: Rohan Joseph
"""



# ============================================================
# Importing Libraries and Utilities
# ============================================================

import os
import sys
import subprocess

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import settings
from src.logger import capture_script_console_to_markdown
from src.harmonization import prepare_ios_disclosures



# ============================================================
# Tests
# ============================================================

def app_meta_frame():
    """
    Build a one-app metadata frame with every metadata column present.
    This lets the prepared frame exercise the metadata merge and match flag.
    """

    return pd.DataFrame(
        {
            "app_id": ["a1"],
            "category_name": ["Productivity"],
            "subcategory_name": ["Tools"],
            "cross_store_app_id": ["c1"],
            "initial_release_date": ["2023-01-01"],
        }
    )


def test_prepare_ios_disclosures_counts_and_matches():
    """
    Check that indicators become 0/1, the disclosure count is right, and metadata is matched.
    This locks the core iOS preparation the harmonization stage consumes.
    """

    ios_df = pd.DataFrame({"app_id": ["a1"], "ind_x": ["1"], "ind_y": ["0"]})

    prepared = prepare_ios_disclosures(ios_df, app_meta_frame(), ["ind_x", "ind_y"])

    assert prepared.loc[0, "ind_x"] == 1
    assert prepared.loc[0, "Disclosure Indicator Count"] == 1
    assert prepared.loc[0, "Metadata Match Found"] == 1
    assert prepared.loc[0, "category_name"] == "Productivity"



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
        script_name = "t002_prepare_ios_privacy_labels",
        log_dir = settings.LOG_DIR,
    )
