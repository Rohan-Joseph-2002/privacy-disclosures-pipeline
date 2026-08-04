"""
AUTHOR: Rohan Joseph
PURPOSE: Test the common-label harmonization — mapping positive iOS indicators through the
         abbreviation map, and Android indicators through the taxonomy and translation maps,
         including the unmapped fallback.
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
from src.harmonization import (
    map_android_disclosures_to_common_labels,
    map_ios_disclosures_to_common_labels,
)



# ============================================================
# Tests
# ============================================================

def test_map_ios_disclosures_maps_positive_indicators():
    """
    Check that a positive iOS indicator melts to a long row and maps to its common label.
    This confirms the iOS side of the shared common-label space.
    """

    ios_df = pd.DataFrame(
        {
            "app_id": ["a1"], "App_Name": ["Alpha"], "Seller": ["Alpha Inc"],
            "category_name": ["Productivity"], "col_x": [1],
        }
    )
    abbreviation_map = pd.DataFrame({"Column Name": ["col_x"], "Common Label": ["Label X"]})

    mapped = map_ios_disclosures_to_common_labels(ios_df, abbreviation_map)

    assert mapped.loc[0, "Common Label"] == "Label X"
    assert mapped.loc[0, "Platform"] == "iOS"


def test_map_android_disclosures_falls_back_to_unmapped():
    """
    Check that an Android indicator with no translation match falls back to UNMAPPED.
    This confirms the fillna fallback on the Android common-label mapping.
    """

    android_df = pd.DataFrame(
        {
            "app_id": ["a1"], "App_Name": ["Gamma"], "Seller": ["Gamma LLC"],
            "category_name": ["Productivity"], "col_y": [1],
        }
    )
    taxonomy_map = pd.DataFrame({"Column Name": ["col_y"], "Item Name": ["Item Y"]})
    translation = pd.DataFrame({"Item Name": ["Item Z"], "Common Label": ["Label Z"]})

    mapped = map_android_disclosures_to_common_labels(android_df, taxonomy_map, translation)

    assert mapped.loc[0, "Common Label"] == settings.UNMAPPED_COMMON_LABEL



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
        script_name = "t004_harmonization",
        log_dir = settings.LOG_DIR,
    )
