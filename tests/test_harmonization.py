"""
AUTHOR: Rohan Joseph
PURPOSE: Unit tests for cross-store harmonization helpers.
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
from disclosures.harmonization import (
    map_android_disclosures_to_common_labels,
    map_ios_disclosures_to_common_labels,
)



"""
Functions
"""

def test_map_ios_disclosures_to_common_labels() -> None:
    """
    Ensure positive iOS indicator columns are mapped into the common-label space.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    ios_df = pd.DataFrame(
        {
            "app_id": ["1001"],
            "App_Name": ["Example App"],
            "Seller": ["Example Seller"],
            "category_name": ["Applications"],
            "DataUsedtoTrackYou_Identifiers_UserID": [1],
        }
    )
    abbreviation_map_df = pd.DataFrame(
        {
            "Column Name": ["DataUsedtoTrackYou_Identifiers_UserID"],
            "Common Label": ["du2tu_Idf_UserID"],
        }
    )

    harmonized_df = map_ios_disclosures_to_common_labels(ios_df, abbreviation_map_df)

    assert harmonized_df["Common Label"].iloc[0] == "du2tu_Idf_UserID"


def test_map_android_disclosures_to_common_labels() -> None:
    """
    Ensure positive Android indicator columns are translated into the common-label space.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    android_df = pd.DataFrame(
        {
            "app_id": ["com.example.app"],
            "App_Name": ["Example App"],
            "Seller": ["Example Seller"],
            "category_name": ["Applications"],
            "Datacollected_Appactivity_Appinteractions_Analytics": [1],
        }
    )
    android_taxonomy_map_df = pd.DataFrame(
        {
            "Column Name": ["Datacollected_Appactivity_Appinteractions_Analytics"],
            "Item Name": ["Data collected_App activity_App interactions_Analytics"],
        }
    )
    translation_df = pd.DataFrame(
        {
            "Item Name": ["Data collected_App activity_App interactions_Analytics"],
            "Common Label": ["dc_Anly_UsgData_PdIa"],
        }
    )

    harmonized_df = map_android_disclosures_to_common_labels(android_df, android_taxonomy_map_df, translation_df)

    assert harmonized_df["Common Label"].iloc[0] == "dc_Anly_UsgData_PdIa"
