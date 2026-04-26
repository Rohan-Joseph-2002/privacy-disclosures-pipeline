"""
AUTHOR: Rohan Joseph
PURPOSE: Summary-statistics helpers for disclosure outputs.
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
from project.settings import UNMAPPED_COMMON_LABEL



"""
Functions
"""

def build_disclosure_summary(prepared_df: pd.DataFrame, platform_label: str) -> pd.DataFrame:
    """
    Build a compact metric summary for a prepared disclosure dataset.
    This helps quick validation and README-facing outputs.
    """

    rows = [
        {
            "section": platform_label,
            "metric": "row_count",
            "value": int(len(prepared_df)),
            "notes": f"Total prepared {platform_label} rows.",
        },
        {
            "section": platform_label,
            "metric": "unique_apps",
            "value": int(prepared_df["app_id"].nunique()),
            "notes": f"Unique app IDs in the prepared {platform_label} dataset.",
        },
        {
            "section": platform_label,
            "metric": "apps_with_any_disclosure",
            "value": int((prepared_df["Disclosure Indicator Count"] > 0).sum()),
            "notes": f"Prepared {platform_label} rows with at least one positive disclosure indicator.",
        },
        {
            "section": platform_label,
            "metric": "metadata_matched_rows",
            "value": int(prepared_df["Metadata Match Found"].sum()),
            "notes": f"Prepared {platform_label} rows matched to the app metadata sample.",
        },
    ]

    return pd.DataFrame(rows)


def build_category_summary(prepared_df: pd.DataFrame, platform_label: str) -> pd.DataFrame:
    """
    Build a category-level summary for a prepared disclosure dataset.
    This helps quick platform-level composition checks.
    """

    category_df = prepared_df.copy()
    category_df["category_name"] = category_df["category_name"].fillna("Unknown")

    summary_df = (
        category_df.groupby("category_name", dropna = False)
        .agg(
            {
                "app_id": "nunique",
                "Disclosure Indicator Count": "mean",
            }
        )
        .reset_index()
        .rename(
            columns = {
                "category_name": "Category Name",
                "app_id": "Unique App Count",
                "Disclosure Indicator Count": "Average Disclosure Indicator Count",
            }
        )
    )
    summary_df.insert(0, "Platform", platform_label)

    return summary_df.sort_values(["Unique App Count", "Category Name"], ascending = [False, True]).reset_index(drop = True)


def build_common_label_summary(
    ios_long_df: pd.DataFrame,
    android_long_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build a cross-platform summary of harmonized common labels.
    This helps comparing disclosure coverage after taxonomy harmonization.
    """

    combined_df = pd.concat([ios_long_df, android_long_df], ignore_index = True)
    combined_df = combined_df[combined_df["Common Label"].fillna("") != ""].copy()
    combined_df = combined_df[combined_df["Common Label"] != UNMAPPED_COMMON_LABEL].copy()

    summary_df = (
        combined_df.groupby(["Common Label", "Platform"], dropna = False)["app_id"]
        .nunique()
        .reset_index(name = "Unique App Count")
        .pivot(index = "Common Label", columns = "Platform", values = "Unique App Count")
        .fillna(0)
        .reset_index()
    )

    if "iOS" not in summary_df.columns:
        summary_df["iOS"] = 0

    if "Android" not in summary_df.columns:
        summary_df["Android"] = 0

    summary_df = summary_df.rename(
        columns = {
            "iOS": "iOS App Count",
            "Android": "Android App Count",
        }
    )
    summary_df["Total App Count"] = summary_df["iOS App Count"] + summary_df["Android App Count"]

    return summary_df.sort_values(["Total App Count", "Common Label"], ascending = [False, True]).reset_index(drop = True)


def build_platform_comparison_summary(
    ios_long_df: pd.DataFrame,
    android_long_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build a compact summary comparing harmonized outputs across platforms.
    This helps README-friendly final metrics.
    """

    rows = [
        {
            "section": "harmonized_ios",
            "metric": "positive_common_label_rows",
            "value": int(len(ios_long_df)),
            "notes": "Positive iOS disclosure rows after mapping to common labels.",
        },
        {
            "section": "harmonized_android",
            "metric": "positive_common_label_rows",
            "value": int(len(android_long_df)),
            "notes": "Positive Android disclosure rows after mapping to common labels.",
        },
        {
            "section": "harmonized_android",
            "metric": "unmapped_rows",
            "value": int((android_long_df["Common Label"] == UNMAPPED_COMMON_LABEL).sum()),
            "notes": "Android disclosure rows without a common-label mapping.",
        },
    ]

    return pd.DataFrame(rows)
