"""
AUTHOR: Rohan Joseph
PURPOSE: Stage 1 pipeline for preparing taxonomy and reference inputs.
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
from disclosures.taxonomies import (
    build_platform_registry_summary,
    build_privacy_labels_map,
    build_safety_forms_map,
    construct_privacy_labels_dict,
    construct_safety_forms_dict,
    prepare_android_to_ios_translation_map,
    prepare_privacy_label_abbreviation_map,
)
from project.io import read_csv_dataframe, read_excel_dataframe, write_csv_dataframe
from project.utils import print_section_header, print_status
from project.validation import require_columns



"""
Functions
"""

def run_prepare_reference_data(config, paths) -> None:
    """
    Prepare taxonomy and reference inputs for downstream stage execution.
    This keeps execution flow centralized instead of spreading stage orchestration across multiple callers.
    """

    print_section_header("Loading Reference Inputs")
    translation_df = read_csv_dataframe(config.android_to_ios_map_path)
    abbreviation_df = read_excel_dataframe(config.privacy_label_abbreviations_path)
    app_meta_df = read_csv_dataframe(config.app_meta_path)
    log_sheet_df = read_csv_dataframe(config.app_log_sheet_path)

    print_status(f"Loaded Android-to-iOS map shape: {translation_df.shape}.")
    print_status(f"Loaded abbreviation map shape: {abbreviation_df.shape}.")
    print_status(f"Loaded app metadata shape: {app_meta_df.shape}.")
    print_status(f"Loaded app log sheet shape: {log_sheet_df.shape}.")

    require_columns(translation_df, ["item_name", "label"], "Android-to-iOS translation map")
    require_columns(app_meta_df, ["app_id", "category_name", "subcategory_name"], "app metadata")

    print_section_header("Preparing Taxonomy Maps")
    ios_taxonomy_map_df = build_privacy_labels_map(construct_privacy_labels_dict())
    android_taxonomy_map_df = build_safety_forms_map(construct_safety_forms_dict())
    prepared_abbreviation_df = prepare_privacy_label_abbreviation_map(abbreviation_df)
    prepared_translation_df = prepare_android_to_ios_translation_map(translation_df)
    platform_registry_summary_df = build_platform_registry_summary(log_sheet_df)

    print_status(f"Prepared iOS taxonomy map shape: {ios_taxonomy_map_df.shape}.")
    print_status(f"Prepared Android taxonomy map shape: {android_taxonomy_map_df.shape}.")
    print_status(f"Prepared abbreviation map shape: {prepared_abbreviation_df.shape}.")
    print_status(f"Prepared translation map shape: {prepared_translation_df.shape}.")
    print_status(f"Prepared platform registry summary shape: {platform_registry_summary_df.shape}.")

    print_section_header("Exporting Stage Outputs")
    write_csv_dataframe(ios_taxonomy_map_df, os.path.join(paths.stage_001_dir, "ios_privacy_labels_map.csv"))
    write_csv_dataframe(android_taxonomy_map_df, os.path.join(paths.stage_001_dir, "android_safety_forms_map.csv"))
    write_csv_dataframe(prepared_abbreviation_df, os.path.join(paths.stage_001_dir, "privacy_label_abbreviation_map.csv"))
    write_csv_dataframe(prepared_translation_df, os.path.join(paths.stage_001_dir, "prepared_taxonomy_translation_map.csv"))
    write_csv_dataframe(app_meta_df, os.path.join(paths.stage_001_dir, "prepared_app_metadata.csv"))
    write_csv_dataframe(platform_registry_summary_df, os.path.join(paths.stage_001_dir, "platform_registry_summary.csv"))

    print_status("Exported stage outputs: ios_privacy_labels_map.csv, android_safety_forms_map.csv, privacy_label_abbreviation_map.csv, prepared_taxonomy_translation_map.csv, prepared_app_metadata.csv, platform_registry_summary.csv.")
