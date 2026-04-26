"""
AUTHOR: Rohan Joseph
PURPOSE: Stage 4 pipeline for harmonizing iOS and Android disclosures into a shared taxonomy.
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
from analysis.summary_statistics import (
    build_common_label_summary,
    build_platform_comparison_summary,
)
from disclosures.harmonization import (
    map_android_disclosures_to_common_labels,
    map_ios_disclosures_to_common_labels,
)
from project.io import read_csv_dataframe, write_csv_dataframe
from project.utils import print_section_header, print_status



"""
Functions
"""

def run_harmonize_cross_store_disclosures(config, paths) -> None:
    """
    Harmonize iOS and Android disclosures into a shared common-label space.
    This keeps execution flow centralized instead of spreading stage orchestration across multiple callers.
    """

    print_section_header("Loading Prepared Inputs")
    prepared_ios_df = read_csv_dataframe(os.path.join(paths.stage_002_dir, "prepared_ios_privacy_labels.csv"))
    prepared_android_df = read_csv_dataframe(os.path.join(paths.stage_003_dir, "prepared_android_safety_forms.csv"))
    abbreviation_map_df = read_csv_dataframe(os.path.join(paths.stage_001_dir, "privacy_label_abbreviation_map.csv"))
    android_taxonomy_map_df = read_csv_dataframe(os.path.join(paths.stage_001_dir, "android_safety_forms_map.csv"))
    translation_df = read_csv_dataframe(os.path.join(paths.stage_001_dir, "prepared_taxonomy_translation_map.csv"))

    print_status(f"Loaded prepared iOS disclosure shape: {prepared_ios_df.shape}.")
    print_status(f"Loaded prepared Android disclosure shape: {prepared_android_df.shape}.")

    print_section_header("Building Harmonized Outputs")
    harmonized_ios_df = map_ios_disclosures_to_common_labels(prepared_ios_df, abbreviation_map_df)
    harmonized_android_df = map_android_disclosures_to_common_labels(
        prepared_android_df,
        android_taxonomy_map_df,
        translation_df,
    )
    common_label_summary_df = build_common_label_summary(harmonized_ios_df, harmonized_android_df)
    platform_comparison_summary_df = build_platform_comparison_summary(harmonized_ios_df, harmonized_android_df)

    print_status(f"Harmonized iOS disclosure shape: {harmonized_ios_df.shape}.")
    print_status(f"Harmonized Android disclosure shape: {harmonized_android_df.shape}.")
    print_status(f"Common-label summary shape: {common_label_summary_df.shape}.")
    print_status(f"Platform comparison summary shape: {platform_comparison_summary_df.shape}.")

    print_section_header("Exporting Stage Outputs")
    write_csv_dataframe(harmonized_ios_df, os.path.join(paths.stage_004_dir, "harmonized_ios_disclosures_long.csv"))
    write_csv_dataframe(harmonized_android_df, os.path.join(paths.stage_004_dir, "harmonized_android_disclosures_long.csv"))
    write_csv_dataframe(common_label_summary_df, os.path.join(paths.stage_004_dir, "cross_platform_common_label_summary.csv"))
    write_csv_dataframe(platform_comparison_summary_df, os.path.join(paths.stage_004_dir, "platform_disclosure_summary.csv"))

    print_status("Exported stage outputs: harmonized_ios_disclosures_long.csv, harmonized_android_disclosures_long.csv, cross_platform_common_label_summary.csv, platform_disclosure_summary.csv.")
