"""
AUTHOR: Rohan Joseph
PURPOSE: Stage 2 pipeline for preparing iOS privacy-label disclosures.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os
# --- Import project-specific utilities and pipeline code ---
from analysis.summary_statistics import build_category_summary, build_disclosure_summary
from disclosures.harmonization import identify_indicator_columns, prepare_ios_disclosures
from project.io import read_csv_dataframe, write_csv_dataframe
from project.settings import IOS_BASE_COLUMNS, IOS_STATUS_COLUMNS
from project.utils import print_section_header, print_status
from project.validation import require_columns



"""
Functions
"""

def run_prepare_ios_privacy_labels(config, paths) -> None:
    """
    Prepare the iOS privacy-label sample and related stage summaries.
    This keeps execution flow centralized instead of spreading stage orchestration across multiple callers.
    """

    print_section_header("Loading Inputs")
    ios_df = read_csv_dataframe(config.ios_privacy_labels_path, max_rows = config.max_ios_rows)
    app_meta_df = read_csv_dataframe(os.path.join(paths.stage_001_dir, "prepared_app_metadata.csv"))
    ios_taxonomy_map_df = read_csv_dataframe(os.path.join(paths.stage_001_dir, "ios_privacy_labels_map.csv"))

    print_status(f"Loaded raw iOS privacy-label sample shape: {ios_df.shape}.")
    print_status(f"Loaded prepared app metadata shape: {app_meta_df.shape}.")

    require_columns(ios_df, IOS_BASE_COLUMNS + IOS_STATUS_COLUMNS, "raw iOS privacy-label sample")

    print_section_header("Preparing iOS Disclosure Data")
    indicator_columns = identify_indicator_columns(
        ios_df,
        ios_taxonomy_map_df["Column Name"].tolist() + IOS_STATUS_COLUMNS,
    )
    prepared_ios_df = prepare_ios_disclosures(
        ios_df = ios_df,
        app_meta_df = app_meta_df,
        indicator_columns = indicator_columns,
    )
    ios_disclosure_summary_df = build_disclosure_summary(prepared_ios_df, "ios")
    ios_category_summary_df = build_category_summary(prepared_ios_df, "iOS")

    print_status(f"Prepared iOS disclosure shape: {prepared_ios_df.shape}.")
    print_status(f"Prepared iOS summary shape: {ios_disclosure_summary_df.shape}.")
    print_status(f"Prepared iOS category summary shape: {ios_category_summary_df.shape}.")

    print_section_header("Exporting Stage Outputs")
    write_csv_dataframe(prepared_ios_df, os.path.join(paths.stage_002_dir, "prepared_ios_privacy_labels.csv"))
    write_csv_dataframe(ios_disclosure_summary_df, os.path.join(paths.stage_002_dir, "ios_disclosure_summary.csv"))
    write_csv_dataframe(ios_category_summary_df, os.path.join(paths.stage_002_dir, "ios_category_summary.csv"))

    print_status("Exported stage outputs: prepared_ios_privacy_labels.csv, ios_disclosure_summary.csv, ios_category_summary.csv.")
