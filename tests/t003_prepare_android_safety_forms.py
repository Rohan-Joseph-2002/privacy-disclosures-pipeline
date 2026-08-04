"""
AUTHOR: Rohan Joseph
PURPOSE: Test the Android disclosure preparation — collapsing repeated app rows to one profile per
         app with a max-aggregated indicator, and the per-row disclosure count.
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
from src.harmonization import prepare_android_disclosures



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


def test_prepare_android_disclosures_dedups_and_max_aggregates():
    """
    Check that two rows for one app collapse to a single row with the indicator max-aggregated.
    This locks the Android dedup behaviour before harmonization.
    """

    android_df = pd.DataFrame(
        {
            "app_id": ["a1", "a1"],
            "Platform": ["Android", "Android"],
            "App_Name": ["Gamma", "Gamma"],
            "Seller": ["Gamma LLC", "Gamma LLC"],
            "Safety_Forms": ["forms", "forms"],
            "URL": ["u", "u"],
            "ind_x": ["0", "1"],
        }
    )

    prepared = prepare_android_disclosures(android_df, app_meta_frame(), ["ind_x"])

    assert len(prepared) == 1
    assert prepared.loc[0, "ind_x"] == 1
    assert prepared.loc[0, "Disclosure Indicator Count"] == 1



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
        script_name = "t003_prepare_android_safety_forms",
        log_dir = settings.LOG_DIR,
    )
