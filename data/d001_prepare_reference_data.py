"""
AUTHOR: Rohan Joseph
PURPOSE: Reconstruct the iOS and Android disclosure taxonomies and prepare the cross-platform
         reference tables — the abbreviation map (read from an Excel file), the Android-to-iOS
         translation map, the app metadata, and a platform registry summary — writing them all to
         data-output for the disclosure stages.
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

from src import io, settings, taxonomies, validation
from src.logger import capture_script_console_to_markdown
from src.utils import print_section_header, print_stage_banner, print_status



# ============================================================
# Settings
# ============================================================

IOS_MAP_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d001_ios_privacy_labels_map.csv")
ANDROID_MAP_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d001_android_safety_forms_map.csv")
ABBREVIATION_MAP_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d001_privacy_label_abbreviation_map.csv"
)
TRANSLATION_MAP_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d001_prepared_taxonomy_translation_map.csv"
)
APP_METADATA_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d001_prepared_app_metadata.csv")
REGISTRY_SUMMARY_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d001_platform_registry_summary.csv")



# ============================================================
# Main Execution
# ============================================================

def run():
    """
    Load the reference inputs, build the taxonomy and reference maps, and write them.
    This is the stage entry point for both run_all.py and standalone manual runs.
    """

    print_section_header("Loading Reference Inputs")

    validation.require_existing_file(settings.ANDROID_TO_IOS_MAP_PATH, context = "translation map")
    validation.require_existing_file(settings.ABBREVIATIONS_PATH, context = "abbreviation workbook")
    validation.require_existing_file(settings.APP_META_PATH, context = "app metadata")
    validation.require_existing_file(settings.APP_LOG_SHEET_PATH, context = "app log sheet")

    translation_df = io.read_csv(settings.ANDROID_TO_IOS_MAP_PATH, keep_empty_as_str = True)
    abbreviation_df = pd.read_excel(settings.ABBREVIATIONS_PATH)
    app_meta_df = io.read_csv(settings.APP_META_PATH, keep_empty_as_str = True)
    log_sheet_df = io.read_csv(settings.APP_LOG_SHEET_PATH, keep_empty_as_str = True)

    validation.require_columns(translation_df, ["item_name", "label"], context = "translation map")
    validation.require_columns(app_meta_df, settings.APP_META_COLUMNS, context = "app metadata")

    print_status(f"Loaded translation {translation_df.shape} and app metadata {app_meta_df.shape}.")

    print_section_header("Building Taxonomy and Reference Maps")

    ios_map_df = taxonomies.build_privacy_labels_map(taxonomies.construct_privacy_labels_dict())
    android_map_df = taxonomies.build_safety_forms_map(taxonomies.construct_safety_forms_dict())
    abbreviation_map_df = taxonomies.prepare_privacy_label_abbreviation_map(abbreviation_df)
    prepared_translation_df = taxonomies.prepare_android_to_ios_translation_map(translation_df)
    registry_summary_df = taxonomies.build_platform_registry_summary(log_sheet_df)

    io.write_csv(ios_map_df, IOS_MAP_PATH)
    io.write_csv(android_map_df, ANDROID_MAP_PATH)
    io.write_csv(abbreviation_map_df, ABBREVIATION_MAP_PATH)
    io.write_csv(prepared_translation_df, TRANSLATION_MAP_PATH)
    io.write_csv(app_meta_df, APP_METADATA_PATH)
    io.write_csv(registry_summary_df, REGISTRY_SUMMARY_PATH)

    print_status(f"Built iOS map {ios_map_df.shape} and Android map {android_map_df.shape}.")


def main():
    """
    Run the reference data preparation stage behind a labelled banner.
    This gives the stage one predictable entry point that also reads well in the logs.
    """

    print_stage_banner("Data 001 | Prepare Reference Data")
    run()


if __name__ == "__main__":
    capture_script_console_to_markdown(
        run_callable = main,
        script_name = "d001_prepare_reference_data",
        log_dir = settings.LOG_DIR,
    )
