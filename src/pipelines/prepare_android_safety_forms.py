"""
AUTHOR: Rohan Joseph
PURPOSE: Stage 3 pipeline for preparing Android safety-form disclosures.
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
from disclosures.harmonization import identify_indicator_columns, prepare_android_disclosures
from project.io import read_csv_dataframe, write_csv_dataframe
from project.settings import ANDROID_BASE_COLUMNS, ANDROID_STATUS_COLUMNS
from project.utils import print_section_header, print_status
from project.validation import require_columns



"""
Functions
"""

def run_prepare_android_safety_forms(config, paths) -> None:
    """
    Prepare the Android safety-form sample and related stage summaries.
    This keeps execution flow centralized instead of spreading stage orchestration across multiple callers.
    """

    print_section_header("Loading Inputs")
    android_df = read_csv_dataframe(config.android_safety_forms_path, max_rows = config.max_android_rows)
    app_meta_df = read_csv_dataframe(os.path.join(paths.stage_001_dir, "prepared_app_metadata.csv"))
    android_taxonomy_map_df = read_csv_dataframe(os.path.join(paths.stage_001_dir, "android_safety_forms_map.csv"))

    print_status(f"Loaded raw Android safety-form sample shape: {android_df.shape}.")
    print_status(f"Loaded prepared app metadata shape: {app_meta_df.shape}.")

    require_columns(android_df, ANDROID_BASE_COLUMNS + ANDROID_STATUS_COLUMNS, "raw Android safety-form sample")

    print_section_header("Preparing Android Disclosure Data")
    indicator_columns = identify_indicator_columns(
        android_df,
        android_taxonomy_map_df["Column Name"].tolist(),
    )
    prepared_android_df = prepare_android_disclosures(
        android_df = android_df,
        app_meta_df = app_meta_df,
        indicator_columns = indicator_columns,
    )
    android_disclosure_summary_df = build_disclosure_summary(prepared_android_df, "android")
    android_category_summary_df = build_category_summary(prepared_android_df, "Android")

    print_status(f"Prepared Android disclosure shape: {prepared_android_df.shape}.")
    print_status(f"Prepared Android summary shape: {android_disclosure_summary_df.shape}.")
    print_status(f"Prepared Android category summary shape: {android_category_summary_df.shape}.")

    print_section_header("Exporting Stage Outputs")
    write_csv_dataframe(prepared_android_df, os.path.join(paths.stage_003_dir, "prepared_android_safety_forms.csv"))
    write_csv_dataframe(android_disclosure_summary_df, os.path.join(paths.stage_003_dir, "android_disclosure_summary.csv"))
    write_csv_dataframe(android_category_summary_df, os.path.join(paths.stage_003_dir, "android_category_summary.csv"))

    print_status("Exported stage outputs: prepared_android_safety_forms.csv, android_disclosure_summary.csv, android_category_summary.csv.")
