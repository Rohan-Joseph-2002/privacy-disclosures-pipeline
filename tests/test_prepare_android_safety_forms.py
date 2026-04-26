"""
AUTHOR: Rohan Joseph
PURPOSE: Unit tests for Android disclosure preparation helpers.
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
from disclosures.harmonization import prepare_android_disclosures



"""
Functions
"""

def test_prepare_android_disclosures_collapses_duplicate_rows() -> None:
    """
    Ensure the Android preparation step collapses repeated app rows and preserves positive indicators.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    android_df = pd.DataFrame(
        {
            "app_id": ["com.example.app", "com.example.app"],
            "Platform": ["Android", "Android"],
            "App_Name": ["", "Example App"],
            "Seller": ["", "Example Seller"],
            "Safety_Forms": ["Form A", "Form A"],
            "URL": ["https://example.com", "https://example.com"],
            "Nodatacollected": [0, 0],
            "Nodatasharedwiththirdparties": [0, 0],
            "Datashared_Location_Approximatelocation_Analytics": [1, 0],
        }
    )
    app_meta_df = pd.DataFrame(
        {
            "app_id": ["com.example.app"],
            "category_name": ["Applications"],
            "subcategory_name": ["Productivity"],
            "cross_store_app_id": [None],
            "initial_release_date": ["01jan2020"],
        }
    )

    prepared_df = prepare_android_disclosures(
        android_df = android_df,
        app_meta_df = app_meta_df,
        indicator_columns = [
            "Nodatacollected",
            "Nodatasharedwiththirdparties",
            "Datashared_Location_Approximatelocation_Analytics",
        ],
    )

    assert len(prepared_df) == 1
    assert prepared_df["App_Name"].iloc[0] == "Example App"
    assert prepared_df["Disclosure Indicator Count"].iloc[0] == 1
