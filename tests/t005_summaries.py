"""
AUTHOR: Rohan Joseph
PURPOSE: Test the Analysis 1 summary builders — the per-platform disclosure metrics, the
         cross-platform common-label comparison, and the platform-comparison metric table.
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
from analysis.a001_build_summaries import (
    build_common_label_summary,
    build_disclosure_summary,
    build_platform_comparison_summary,
)



# ============================================================
# Tests
# ============================================================

def ios_long_frame():
    """
    Build a one-row harmonized iOS long frame for the summary tests.
    This gives the cross-platform summaries a known iOS contribution.
    """

    return pd.DataFrame(
        {"Common Label": ["Usage Analytics"], "Platform": ["iOS"], "app_id": ["a1"]}
    )


def android_long_frame():
    """
    Build a harmonized Android long frame with one mapped and one unmapped row.
    This gives the summaries a shared label plus an unmapped fallback to count.
    """

    return pd.DataFrame(
        {
            "Common Label": ["Usage Analytics", settings.UNMAPPED_COMMON_LABEL],
            "Platform": ["Android", "Android"],
            "app_id": ["b1", "b2"],
        }
    )


def value_of(summary_df, metric):
    """
    Return the value for a given metric from a metric-style summary table.
    This reads a single metric cell without depending on row order.
    """

    return summary_df[summary_df["metric"] == metric]["value"].iloc[0]


def test_disclosure_summary_reports_counts():
    """
    Check that the disclosure summary reports rows, unique apps, disclosures, and matches.
    This locks the per-platform validation snapshot.
    """

    prepared = pd.DataFrame(
        {
            "app_id": ["a1", "a2"],
            "Disclosure Indicator Count": [2, 0],
            "Metadata Match Found": [1, 1],
        }
    )

    summary = build_disclosure_summary(prepared, "ios")

    assert value_of(summary, "row_count") == 2
    assert value_of(summary, "apps_with_any_disclosure") == 1
    assert value_of(summary, "metadata_matched_rows") == 2


def test_common_label_summary_counts_shared_label():
    """
    Check that a label on both platforms is counted for each and totalled, excluding UNMAPPED.
    This confirms the cross-platform comparison after harmonization.
    """

    summary = build_common_label_summary(ios_long_frame(), android_long_frame())
    row = summary[summary["Common Label"] == "Usage Analytics"].iloc[0]

    assert row["Total App Count"] == 2
    assert settings.UNMAPPED_COMMON_LABEL not in set(summary["Common Label"])


def test_platform_comparison_counts_unmapped():
    """
    Check that the platform comparison counts positive rows per platform and unmapped rows.
    This locks the harmonization metric snapshot.
    """

    comparison = build_platform_comparison_summary(ios_long_frame(), android_long_frame())

    assert value_of(comparison, "unmapped_rows") == 1



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
        script_name = "t005_summaries",
        log_dir = settings.LOG_DIR,
    )
