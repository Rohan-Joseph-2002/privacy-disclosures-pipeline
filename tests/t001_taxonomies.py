"""
AUTHOR: Rohan Joseph
PURPOSE: Test the taxonomy builders and reference-map preparation — the iOS and Android taxonomy
         maps' column names, the abbreviation map, and the Android-to-iOS translation map.
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
from src.taxonomies import (
    build_privacy_labels_map,
    build_safety_forms_map,
    construct_privacy_labels_dict,
    construct_safety_forms_dict,
    prepare_android_to_ios_translation_map,
    prepare_privacy_label_abbreviation_map,
)



# ============================================================
# Tests
# ============================================================

def test_build_privacy_labels_map_includes_expected_columns():
    """
    Check that the iOS taxonomy map contains a known compact indicator column name.
    This locks the wide-column naming convention the harmonization relies on.
    """

    ios_map = build_privacy_labels_map(construct_privacy_labels_dict())

    assert "DataUsedtoTrackYou_Identifiers_UserID" in set(ios_map["Column Name"])


def test_build_safety_forms_map_includes_status_and_paths():
    """
    Check that the Android taxonomy map has the status columns and a data-path column.
    This confirms both the appended status rows and the generated path rows are present.
    """

    android_map = build_safety_forms_map(construct_safety_forms_dict())
    column_names = set(android_map["Column Name"])

    assert "Nodatacollected" in column_names
    assert "Datacollected_Appactivity_Appinteractions_Analytics" in column_names


def test_prepare_abbreviation_map_builds_column_name():
    """
    Check that the abbreviation map keeps the first two columns and rebuilds the column name.
    This is the iOS source-term to common-label bridge used in harmonization.
    """

    raw = pd.DataFrame(
        {"Source Term": ["DataUsedtoTrackYou_Identifiers_UserID"], "Common Label": ["Ids"]}
    )

    prepared = prepare_privacy_label_abbreviation_map(raw)

    assert prepared.loc[0, "Column Name"] == "DataUsedtoTrackYou_Identifiers_UserID"
    assert prepared.loc[0, "Common Label"] == "Ids"


def test_prepare_translation_map_renames_columns():
    """
    Check that the translation map renames its raw columns to the harmonization schema.
    This gives the Android track its item-name to common-label mapping.
    """

    raw = pd.DataFrame(
        {
            "item_name": ["Item A"], "lab1": ["a"], "lab2": ["b"],
            "lab3": ["c"], "lab4": ["d"], "label": ["Common A"],
        }
    )

    prepared = prepare_android_to_ios_translation_map(raw)

    assert list(prepared.columns)[:2] == ["Item Name", "Lab 1"]
    assert prepared.loc[0, "Common Label"] == "Common A"



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
        script_name = "t001_taxonomies",
        log_dir = settings.LOG_DIR,
    )
