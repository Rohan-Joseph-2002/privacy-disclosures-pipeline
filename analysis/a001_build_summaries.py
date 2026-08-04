"""
AUTHOR: Rohan Joseph
PURPOSE: Summarize the prepared and harmonized disclosure outputs — per-platform disclosure and
         category summaries, a cross-platform common-label comparison, and a platform-comparison
         metric table — writing the summaries to analysis-output.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-08-04
MODIFIED BY: Rohan Joseph
"""



# ============================================================
# Importing Libraries and Utilities
# ============================================================

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import io, settings, validation
from src.logger import capture_script_console_to_markdown
from src.utils import print_section_header, print_stage_banner, print_status



# ============================================================
# Settings
# ============================================================

PREPARED_IOS_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d002_prepared_ios_privacy_labels.csv")
PREPARED_ANDROID_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d003_prepared_android_safety_forms.csv"
)
HARMONIZED_IOS_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d004_harmonized_ios_disclosures_long.csv"
)
HARMONIZED_ANDROID_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d004_harmonized_android_disclosures_long.csv"
)

IOS_DISCLOSURE_SUMMARY_PATH = os.path.join(
    settings.ANALYSIS_OUTPUT_DIR, "a001_ios_disclosure_summary.csv"
)
IOS_CATEGORY_SUMMARY_PATH = os.path.join(
    settings.ANALYSIS_OUTPUT_DIR, "a001_ios_category_summary.csv"
)
ANDROID_DISCLOSURE_SUMMARY_PATH = os.path.join(
    settings.ANALYSIS_OUTPUT_DIR, "a001_android_disclosure_summary.csv"
)
ANDROID_CATEGORY_SUMMARY_PATH = os.path.join(
    settings.ANALYSIS_OUTPUT_DIR, "a001_android_category_summary.csv"
)
COMMON_LABEL_SUMMARY_PATH = os.path.join(
    settings.ANALYSIS_OUTPUT_DIR, "a001_cross_platform_common_label_summary.csv"
)
PLATFORM_SUMMARY_PATH = os.path.join(
    settings.ANALYSIS_OUTPUT_DIR, "a001_platform_disclosure_summary.csv"
)



# ============================================================
# Functions
# ============================================================

def summary_row(section, metric, value, notes):
    """
    Build one summary record with a section, metric, value, and note.
    This keeps the metric-style summary builders compact and their row shape consistent.
    """

    return {"section": section, "metric": metric, "value": value, "notes": notes}


def build_disclosure_summary(prepared_df, platform_label):
    """
    Build a compact metric summary for a prepared per-platform disclosure dataset.
    This gives a quick validation snapshot of rows, apps, disclosures, and metadata matches.
    """

    with_disclosure = int((prepared_df["Disclosure Indicator Count"] > 0).sum())
    metadata_matched = int(prepared_df["Metadata Match Found"].sum())

    rows = [
        summary_row(platform_label, "row_count", len(prepared_df), "Total prepared rows."),
        summary_row(
            platform_label, "unique_apps", int(prepared_df["app_id"].nunique()), "Unique app IDs."
        ),
        summary_row(
            platform_label, "apps_with_any_disclosure", with_disclosure, "Positive-disclosure rows."
        ),
        summary_row(
            platform_label, "metadata_matched_rows", metadata_matched, "Metadata-matched rows."
        ),
    ]

    return pd.DataFrame(rows)


def build_category_summary(prepared_df, platform_label):
    """
    Build a category-level summary of app counts and mean disclosure counts.
    This gives a quick view of per-category disclosure composition on one platform.
    """

    category_df = prepared_df.copy()
    category_names = category_df["category_name"].fillna("Unknown")
    category_df["category_name"] = category_names.replace("", "Unknown")

    grouped = category_df.groupby("category_name", dropna = False).agg(
        {"app_id": "nunique", "Disclosure Indicator Count": "mean"}
    )
    grouped = grouped.reset_index().rename(
        columns = {
            "category_name": "Category Name",
            "app_id": "Unique App Count",
            "Disclosure Indicator Count": "Average Disclosure Indicator Count",
        }
    )
    grouped.insert(0, "Platform", platform_label)
    grouped = grouped.sort_values(["Unique App Count", "Category Name"], ascending = [False, True])

    return grouped.reset_index(drop = True)


def build_common_label_summary(ios_long_df, android_long_df):
    """
    Build a cross-platform summary of harmonized common labels by app count.
    This compares disclosure coverage across platforms after taxonomy harmonization.
    """

    combined_df = pd.concat([ios_long_df, android_long_df], ignore_index = True)
    combined_df = combined_df[combined_df["Common Label"].fillna("") != ""]
    combined_df = combined_df[combined_df["Common Label"] != settings.UNMAPPED_COMMON_LABEL]

    counts = combined_df.groupby(["Common Label", "Platform"], dropna = False)["app_id"].nunique()
    summary_df = counts.reset_index(name = "Unique App Count")
    summary_df = summary_df.pivot(
        index = "Common Label", columns = "Platform", values = "Unique App Count"
    ).fillna(0).reset_index()

    for platform in ["iOS", "Android"]:
        if platform not in summary_df.columns:
            summary_df[platform] = 0

    summary_df = summary_df.rename(
        columns = {"iOS": "iOS App Count", "Android": "Android App Count"}
    )
    summary_df["Total App Count"] = summary_df["iOS App Count"] + summary_df["Android App Count"]
    summary_df = summary_df.sort_values(
        ["Total App Count", "Common Label"], ascending = [False, True]
    )

    return summary_df.reset_index(drop = True)


def build_platform_comparison_summary(ios_long_df, android_long_df):
    """
    Build a compact metric summary comparing the two harmonized platform outputs.
    This reports positive-label rows per platform and Android rows left unmapped.
    """

    unmapped = int((android_long_df["Common Label"] == settings.UNMAPPED_COMMON_LABEL).sum())

    rows = [
        summary_row(
            "harmonized_ios", "positive_common_label_rows", len(ios_long_df), "iOS positive rows."
        ),
        summary_row(
            "harmonized_android", "positive_common_label_rows", len(android_long_df),
            "Android positive rows.",
        ),
        summary_row("harmonized_android", "unmapped_rows", unmapped, "Android unmapped rows."),
    ]

    return pd.DataFrame(rows)



# ============================================================
# Main Execution
# ============================================================

def run():
    """
    Load the prepared and harmonized outputs and write the six summary tables.
    This is the stage entry point for both run_all.py and standalone manual runs.
    """

    print_section_header("Loading Prepared and Harmonized Outputs")

    for label, path in [
        ("prepared iOS", PREPARED_IOS_PATH),
        ("prepared Android", PREPARED_ANDROID_PATH),
        ("harmonized iOS", HARMONIZED_IOS_PATH),
        ("harmonized Android", HARMONIZED_ANDROID_PATH),
    ]:
        validation.require_existing_file(path, context = label)

    prepared_ios_df = io.read_csv(PREPARED_IOS_PATH)
    prepared_android_df = io.read_csv(PREPARED_ANDROID_PATH)
    harmonized_ios_df = io.read_csv(HARMONIZED_IOS_PATH)
    harmonized_android_df = io.read_csv(HARMONIZED_ANDROID_PATH)

    print_status(f"Loaded {len(prepared_ios_df)} iOS and {len(prepared_android_df)} Android rows.")

    print_section_header("Building Summary Tables")

    ios_disclosure_df = build_disclosure_summary(prepared_ios_df, "ios")
    ios_category_df = build_category_summary(prepared_ios_df, "iOS")
    android_disclosure_df = build_disclosure_summary(prepared_android_df, "android")
    android_category_df = build_category_summary(prepared_android_df, "Android")

    io.write_csv(ios_disclosure_df, IOS_DISCLOSURE_SUMMARY_PATH)
    io.write_csv(ios_category_df, IOS_CATEGORY_SUMMARY_PATH)
    io.write_csv(android_disclosure_df, ANDROID_DISCLOSURE_SUMMARY_PATH)
    io.write_csv(android_category_df, ANDROID_CATEGORY_SUMMARY_PATH)

    common_label_df = build_common_label_summary(harmonized_ios_df, harmonized_android_df)
    platform_df = build_platform_comparison_summary(harmonized_ios_df, harmonized_android_df)

    io.write_csv(common_label_df, COMMON_LABEL_SUMMARY_PATH)
    io.write_csv(platform_df, PLATFORM_SUMMARY_PATH)

    print_status(f"Wrote 6 summary tables ({len(common_label_df)} common labels).")


def main():
    """
    Run the summary-building stage behind a labelled banner.
    This gives the stage one predictable entry point that also reads well in the logs.
    """

    print_stage_banner("Analysis 001 | Build Disclosure Summaries")
    run()


if __name__ == "__main__":
    capture_script_console_to_markdown(
        run_callable = main,
        script_name = "a001_build_summaries",
        log_dir = settings.LOG_DIR,
    )
