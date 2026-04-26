"""
AUTHOR: Rohan Joseph
PURPOSE: Unit tests for disclosure summary-statistics helpers.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import pandas as pd


# --- Import project-specific utilities and pipeline code ---
from analysis.summary_statistics import build_common_label_summary, build_disclosure_summary



"""
Functions
"""

def test_build_disclosure_summary_reports_basic_metrics() -> None:
    """
    Ensure the prepared-disclosure summary returns core dataset metrics.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    prepared_df = pd.DataFrame(
        {
            "app_id": ["1001", "1002"],
            "Disclosure Indicator Count": [1, 0],
            "Metadata Match Found": [1, 0],
        }
    )

    summary_df = build_disclosure_summary(prepared_df, "ios")

    assert set(summary_df["metric"]) >= {"row_count", "unique_apps", "apps_with_any_disclosure", "metadata_matched_rows"}


def test_build_common_label_summary_combines_platform_counts() -> None:
    """
    Ensure the common-label summary combines iOS and Android app counts.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    ios_long_df = pd.DataFrame(
        {
            "app_id": ["1001"],
            "Common Label": ["label_a"],
            "Platform": ["iOS"],
        }
    )
    android_long_df = pd.DataFrame(
        {
            "app_id": ["com.example.app"],
            "Common Label": ["label_a"],
            "Platform": ["Android"],
        }
    )

    summary_df = build_common_label_summary(ios_long_df, android_long_df)

    assert summary_df["Total App Count"].iloc[0] == 2
