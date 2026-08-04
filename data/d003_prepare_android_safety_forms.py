"""
AUTHOR: Rohan Joseph
PURPOSE: Prepare the wide Android safety-form export into a stable app-level table — dedup repeated
         app rows, typed 0/1 indicators, row-level disclosure diagnostics, and attached app
         metadata — and write it to data-output for the harmonization stage.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-08-04
MODIFIED BY: Rohan Joseph
"""



# ============================================================
# Importing Libraries and Utilities
# ============================================================

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import harmonization, io, settings, validation
from src.logger import capture_script_console_to_markdown
from src.utils import print_section_header, print_stage_banner, print_status



# ============================================================
# Settings
# ============================================================

APP_METADATA_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d001_prepared_app_metadata.csv")
ANDROID_MAP_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d001_android_safety_forms_map.csv")
PREPARED_ANDROID_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d003_prepared_android_safety_forms.csv"
)



# ============================================================
# Main Execution
# ============================================================

def run():
    """
    Load the Android export and reference maps, prepare the disclosure table, and write it.
    This is the stage entry point for both run_all.py and standalone manual runs.
    """

    print_section_header("Loading Inputs")

    validation.require_existing_file(settings.ANDROID_SAFETY_FORMS_PATH, context = "Android sample")
    validation.require_existing_file(APP_METADATA_PATH, context = "prepared app metadata")
    validation.require_existing_file(ANDROID_MAP_PATH, context = "Android taxonomy map")

    android_df = io.read_csv(settings.ANDROID_SAFETY_FORMS_PATH, keep_empty_as_str = True)
    app_meta_df = io.read_csv(APP_METADATA_PATH, keep_empty_as_str = True)
    android_map_df = io.read_csv(ANDROID_MAP_PATH, keep_empty_as_str = True)

    if settings.MAX_ANDROID_ROWS is not None:
        android_df = android_df.head(settings.MAX_ANDROID_ROWS).copy()

    required_columns = settings.ANDROID_BASE_COLUMNS + settings.ANDROID_STATUS_COLUMNS
    validation.require_columns(android_df, required_columns, context = "raw Android sample")

    print_status(f"Loaded {len(android_df)} raw Android rows.")

    print_section_header("Preparing Android Disclosure Data")

    candidate_columns = android_map_df["Column Name"].tolist()
    indicator_columns = harmonization.identify_indicator_columns(android_df, candidate_columns)
    prepared_android_df = harmonization.prepare_android_disclosures(
        android_df, app_meta_df, indicator_columns
    )

    io.write_csv(prepared_android_df, PREPARED_ANDROID_PATH)

    app_count = prepared_android_df["app_id"].nunique()
    print_status(f"Prepared {len(prepared_android_df)} Android rows across {app_count} apps.")


def main():
    """
    Run the Android safety-form preparation stage behind a labelled banner.
    This gives the stage one predictable entry point that also reads well in the logs.
    """

    print_stage_banner("Data 003 | Prepare Android Safety Forms")
    run()


if __name__ == "__main__":
    capture_script_console_to_markdown(
        run_callable = main,
        script_name = "d003_prepare_android_safety_forms",
        log_dir = settings.LOG_DIR,
    )
