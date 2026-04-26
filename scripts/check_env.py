"""
AUTHOR: Rohan Joseph
PURPOSE: Validate local runtime configuration and project dependencies.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os
import sys



"""
Settings
"""

# --- Ensure that the src directory is on PATH ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# --- Import project-specific utilities and pipeline code ---
from project.env import get_runtime_config  # type: ignore
from project.paths import ensure_project_directories  # type: ignore
from project.utils import print_section_header, print_stage_banner, print_status  # type: ignore
from project.validation import require_existing_file  # type: ignore
from project.logger import capture_script_console_to_markdown  # type: ignore



"""
Script
"""

def main() -> None:
    """
    Validate that local configuration, inputs, and output directories are available.
    This gives the script one predictable command-line entrypoint for manual runs and repo-level orchestration.
    """

    config = get_runtime_config()
    paths = ensure_project_directories()

    print_stage_banner("Checking Runtime Environment")

    print_section_header("Resolved Configuration")
    print_status(f"Runtime mode: {config.runtime_mode}")
    print_status(f"iOS privacy labels path: {config.ios_privacy_labels_path}")
    print_status(f"Android safety forms path: {config.android_safety_forms_path}")
    print_status(f"Android-to-iOS map path: {config.android_to_ios_map_path}")
    print_status(f"Privacy label abbreviations path: {config.privacy_label_abbreviations_path}")
    print_status(f"App metadata path: {config.app_meta_path}")
    print_status(f"App log sheet path: {config.app_log_sheet_path}")
    print_status(f"Max iOS rows: {config.max_ios_rows}")
    print_status(f"Max Android rows: {config.max_android_rows}")

    require_existing_file(config.ios_privacy_labels_path, "iOS privacy-label sample")
    require_existing_file(config.android_safety_forms_path, "Android safety-form sample")
    require_existing_file(config.android_to_ios_map_path, "Android-to-iOS translation map")
    require_existing_file(config.privacy_label_abbreviations_path, "privacy-label abbreviations file")
    require_existing_file(config.app_meta_path, "app metadata sample")
    require_existing_file(config.app_log_sheet_path, "app log sheet sample")

    print_section_header("Output Directories")
    print_status(f"Stage 1 directory: {paths.stage_001_dir}")
    print_status(f"Stage 2 directory: {paths.stage_002_dir}")
    print_status(f"Stage 3 directory: {paths.stage_003_dir}")
    print_status(f"Stage 4 directory: {paths.stage_004_dir}")
    print_status(f"Log directory: {paths.log_dir}")

    print_section_header("Status")
    print_status("Environment check passed.")



"""
Main Execution
"""

if __name__ == "__main__":
    log_path = capture_script_console_to_markdown(
        run_callable = main,
        output_dir = os.path.join(PROJECT_ROOT, "output", "logs"),
        script_name = "check_env",
        also_print_to_console = True,
    )
    print(f"Saved run log to: {log_path}")