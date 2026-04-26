"""
AUTHOR: Rohan Joseph
PURPOSE: Unit tests for iOS disclosure preparation helpers.
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
from disclosures.harmonization import prepare_ios_disclosures



"""
Functions
"""

def test_prepare_ios_disclosures_adds_counts_and_metadata() -> None:
    """
    Ensure the iOS preparation step computes indicator counts and metadata merges.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    ios_df = pd.DataFrame(
        {
            "app_id": ["1001"],
            "Platform": ["iOS"],
            "App_Name": ["Example App"],
            "Seller": ["Example Seller"],
            "Category": ["Utilities"],
            "Price": ["Free"],
            "Languages": ["English"],
            "App_Information": ["Info"],
            "Version_History": ["History"],
            "Privacy_Labels": ["Labels"],
            "URL": ["https://example.com"],
            "NoDetailsProvided": [0],
            "DataNotCollected": [0],
            "DataUsedtoTrackYou_Identifiers_UserID": [1],
        }
    )
    app_meta_df = pd.DataFrame(
        {
            "app_id": ["1001"],
            "category_name": ["Applications"],
            "subcategory_name": ["Utilities"],
            "cross_store_app_id": ["2001"],
            "initial_release_date": ["01jan2020"],
        }
    )

    prepared_df = prepare_ios_disclosures(
        ios_df = ios_df,
        app_meta_df = app_meta_df,
        indicator_columns = ["NoDetailsProvided", "DataNotCollected", "DataUsedtoTrackYou_Identifiers_UserID"],
    )

    assert prepared_df["Disclosure Indicator Count"].iloc[0] == 1
    assert prepared_df["Metadata Match Found"].iloc[0] == 1
    assert "DataUsedtoTrackYou_Identifiers_UserID" in prepared_df["Positive Disclosure Columns"].iloc[0]
