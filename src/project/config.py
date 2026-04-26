"""
AUTHOR: Rohan Joseph
PURPOSE: Central repository configuration and stage registry.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os



"""
Settings
"""

APP_NAME = "privacy_disclosures_pipeline"

DEFAULT_STAGE_ORDER = [
    "001_prepare_reference_data",
    "002_prepare_ios_privacy_labels",
    "003_prepare_android_safety_forms",
    "004_harmonize_cross_store_disclosures",
]



"""
Functions
"""

def build_stage_script_map(project_root: str) -> dict[str, str]:
    """
    Build the canonical stage-to-script mapping for the repository.
    This helps keep orchestration logic centralized and avoid duplicated script references.
    """

    scripts_dir = os.path.join(project_root, "scripts")

    return {
        "001_prepare_reference_data": os.path.join(scripts_dir, "001_prepare_reference_data.py"),
        "002_prepare_ios_privacy_labels": os.path.join(scripts_dir, "002_prepare_ios_privacy_labels.py"),
        "003_prepare_android_safety_forms": os.path.join(scripts_dir, "003_prepare_android_safety_forms.py"),
        "004_harmonize_cross_store_disclosures": os.path.join(scripts_dir, "004_harmonize_cross_store_disclosures.py"),
    }
