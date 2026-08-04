"""
AUTHOR: Rohan Joseph
PURPOSE: Harmonize the prepared iOS and Android disclosures into a shared common-label space —
         melting each platform's positive indicators to long form and mapping them through the
         abbreviation and translation reference maps — and write both long tables to data-output.
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

PREPARED_IOS_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d002_prepared_ios_privacy_labels.csv")
PREPARED_ANDROID_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d003_prepared_android_safety_forms.csv"
)
ABBREVIATION_MAP_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d001_privacy_label_abbreviation_map.csv"
)
ANDROID_MAP_PATH = os.path.join(settings.DATA_OUTPUT_DIR, "d001_android_safety_forms_map.csv")
TRANSLATION_MAP_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d001_prepared_taxonomy_translation_map.csv"
)
HARMONIZED_IOS_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d004_harmonized_ios_disclosures_long.csv"
)
HARMONIZED_ANDROID_PATH = os.path.join(
    settings.DATA_OUTPUT_DIR, "d004_harmonized_android_disclosures_long.csv"
)



# ============================================================
# Main Execution
# ============================================================

def run():
    """
    Load the prepared disclosures and reference maps, harmonize both platforms, and write them.
    This is the stage entry point for both run_all.py and standalone manual runs.
    """

    print_section_header("Loading Prepared Inputs")

    for label, path in [
        ("prepared iOS", PREPARED_IOS_PATH),
        ("prepared Android", PREPARED_ANDROID_PATH),
        ("abbreviation map", ABBREVIATION_MAP_PATH),
        ("Android taxonomy map", ANDROID_MAP_PATH),
        ("translation map", TRANSLATION_MAP_PATH),
    ]:
        validation.require_existing_file(path, context = label)

    prepared_ios_df = io.read_csv(PREPARED_IOS_PATH, keep_empty_as_str = True)
    prepared_android_df = io.read_csv(PREPARED_ANDROID_PATH, keep_empty_as_str = True)
    abbreviation_map_df = io.read_csv(ABBREVIATION_MAP_PATH, keep_empty_as_str = True)
    android_map_df = io.read_csv(ANDROID_MAP_PATH, keep_empty_as_str = True)
    translation_df = io.read_csv(TRANSLATION_MAP_PATH, keep_empty_as_str = True)

    print_status(f"Loaded {len(prepared_ios_df)} iOS and {len(prepared_android_df)} Android rows.")

    print_section_header("Harmonizing To Common Labels")

    harmonized_ios_df = harmonization.map_ios_disclosures_to_common_labels(
        prepared_ios_df, abbreviation_map_df
    )
    harmonized_android_df = harmonization.map_android_disclosures_to_common_labels(
        prepared_android_df, android_map_df, translation_df
    )

    io.write_csv(harmonized_ios_df, HARMONIZED_IOS_PATH)
    io.write_csv(harmonized_android_df, HARMONIZED_ANDROID_PATH)

    ios_rows = len(harmonized_ios_df)
    print_status(f"Harmonized {ios_rows} iOS and {len(harmonized_android_df)} Android long rows.")


def main():
    """
    Run the cross-store harmonization stage behind a labelled banner.
    This gives the stage one predictable entry point that also reads well in the logs.
    """

    print_stage_banner("Data 004 | Harmonize Cross-Store Disclosures")
    run()


if __name__ == "__main__":
    capture_script_console_to_markdown(
        run_callable = main,
        script_name = "d004_harmonize_cross_store_disclosures",
        log_dir = settings.LOG_DIR,
    )
