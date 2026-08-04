"""
AUTHOR: Rohan Joseph
PURPOSE: Prepare the wide iOS privacy-label export into a stable app-level table — typed 0/1
         indicators, row-level disclosure diagnostics, and attached app metadata — and write it to
         data-output for the harmonization stage.
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
IOS_MAP_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d001_ios_privacy_labels_map.csv")
PREPARED_IOS_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d002_prepared_ios_privacy_labels.csv")



# ============================================================
# Main Execution
# ============================================================

def run():
    """
    Load the iOS export and reference maps, prepare the disclosure table, and write it.
    This is the stage entry point for both run_all.py and standalone manual runs.
    """

    print_section_header("Loading Inputs")

    validation.require_existing_file(settings.IOS_PRIVACY_LABELS_PATH, context = "iOS sample")
    validation.require_existing_file(APP_METADATA_PATH, context = "prepared app metadata")
    validation.require_existing_file(IOS_MAP_PATH, context = "iOS taxonomy map")

    ios_df = io.read_csv(settings.IOS_PRIVACY_LABELS_PATH, keep_empty_as_str = True)
    app_meta_df = io.read_csv(APP_METADATA_PATH, keep_empty_as_str = True)
    ios_map_df = io.read_csv(IOS_MAP_PATH, keep_empty_as_str = True)

    if settings.MAX_IOS_ROWS is not None:
        ios_df = ios_df.head(settings.MAX_IOS_ROWS).copy()

    required_columns = settings.IOS_BASE_COLUMNS + settings.IOS_STATUS_COLUMNS
    validation.require_columns(ios_df, required_columns, context = "raw iOS sample")

    print_status(f"Loaded {len(ios_df)} raw iOS rows.")

    print_section_header("Preparing iOS Disclosure Data")

    candidate_columns = ios_map_df["Column Name"].tolist() + settings.IOS_STATUS_COLUMNS
    indicator_columns = harmonization.identify_indicator_columns(ios_df, candidate_columns)
    prepared_ios_df = harmonization.prepare_ios_disclosures(ios_df, app_meta_df, indicator_columns)

    io.write_csv(prepared_ios_df, PREPARED_IOS_PATH)

    indicator_count = len(indicator_columns)
    print_status(f"Prepared {len(prepared_ios_df)} iOS rows over {indicator_count} indicators.")


def main():
    """
    Run the iOS privacy-label preparation stage behind a labelled banner.
    This gives the stage one predictable entry point that also reads well in the logs.
    """

    print_stage_banner("Data 002 | Prepare iOS Privacy Labels")
    run()


if __name__ == "__main__":
    capture_script_console_to_markdown(
        run_callable = main,
        script_name = "d002_prepare_ios_privacy_labels",
        log_dir = settings.LOG_DIR,
    )
