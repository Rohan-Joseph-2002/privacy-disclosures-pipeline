"""
AUTHOR: Rohan Joseph
PURPOSE: Unit tests for taxonomy construction helpers.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import pandas as pd


# --- Import project-specific utilities and pipeline code ---
from disclosures.taxonomies import (
    build_privacy_labels_map,
    build_safety_forms_map,
    construct_privacy_labels_dict,
    construct_safety_forms_dict,
    prepare_privacy_label_abbreviation_map,
    prepare_android_to_ios_translation_map,
)



"""
Functions
"""

def test_build_privacy_labels_map_contains_expected_column() -> None:
    """
    Ensure the iOS taxonomy map reproduces the expected indicator column structure.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    privacy_map_df = build_privacy_labels_map(construct_privacy_labels_dict())

    assert "DataUsedtoTrackYou_Identifiers_UserID" in set(privacy_map_df["Column Name"])


def test_build_safety_forms_map_contains_expected_item_name() -> None:
    """
    Ensure the Android taxonomy map reproduces the expected item-name structure.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    safety_forms_map_df = build_safety_forms_map(construct_safety_forms_dict())

    assert "Data shared_Location_Approximate location_Account management" in set(safety_forms_map_df["Item Name"])


def test_prepare_abbreviation_and_translation_maps() -> None:
    """
    Ensure the common-label preparation helpers retain the core mapping fields.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    abbreviation_df = pd.DataFrame(
        {
            "raw_term": ["DataUsedtoTrackYou_Contact Info_Name"],
            "abbr": ["du2tu_CtcIf_Name"],
        }
    )
    translation_df = pd.DataFrame(
        {
            "item_name": ["Data collected_App activity_App interactions_Analytics"],
            "lab1": ["dc"],
            "lab2": ["UsgData"],
            "lab3": ["PdIa"],
            "lab4": ["Anly"],
            "label": ["dc_Anly_UsgData_PdIa"],
        }
    )

    prepared_abbreviation_df = prepare_privacy_label_abbreviation_map(abbreviation_df)
    prepared_translation_df = prepare_android_to_ios_translation_map(translation_df)

    assert prepared_abbreviation_df["Column Name"].iloc[0] == "DataUsedtoTrackYou_ContactInfo_Name"
    assert prepared_translation_df["Common Label"].iloc[0] == "dc_Anly_UsgData_PdIa"
