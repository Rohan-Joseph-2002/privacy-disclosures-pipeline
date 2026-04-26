"""
AUTHOR: Rohan Joseph
PURPOSE: Disclosure preparation and harmonization helpers.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""

from __future__ import annotations



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import pandas as pd


# --- Import project-specific utilities and pipeline code ---
from project.settings import UNMAPPED_COMMON_LABEL
from project.utils import (
    build_positive_column_string,
    convert_indicator_columns_to_int,
    first_non_empty_value,
)



"""
Functions
"""

def identify_indicator_columns(dataframe: pd.DataFrame, candidate_columns: list[str]) -> list[str]:
    """
    Identify the indicator columns that are both expected and present.
    This helps robust stage logic when sample data omits some columns.
    """

    return [column for column in candidate_columns if column in dataframe.columns]


def prepare_ios_disclosures(
    ios_df: pd.DataFrame,
    app_meta_df: pd.DataFrame,
    indicator_columns: list[str],
) -> pd.DataFrame:
    """
    Prepare the iOS privacy-label export for downstream analysis.
    This helps stabilizing types, enriching metadata, and computing row-level diagnostics.
    """

    prepared_df = ios_df.copy()
    prepared_df["app_id"] = prepared_df["app_id"].astype(str)

    prepared_df = convert_indicator_columns_to_int(prepared_df, indicator_columns)
    prepared_df = prepared_df.copy()
    # Summarize the disclosure profile per app before attaching cross-store metadata.
    prepared_df["Disclosure Indicator Count"] = prepared_df[indicator_columns].sum(axis = 1)
    prepared_df["Positive Disclosure Columns"] = prepared_df.apply(
        lambda row: build_positive_column_string(row, indicator_columns),
        axis = 1,
    )

    app_meta_prepared = app_meta_df.copy()
    app_meta_prepared["app_id"] = app_meta_prepared["app_id"].astype(str)

    prepared_df = prepared_df.merge(
        app_meta_prepared[
            [
                "app_id",
                "category_name",
                "subcategory_name",
                "cross_store_app_id",
                "initial_release_date",
            ]
        ],
        on = "app_id",
        how = "left",
    )
    prepared_df["Metadata Match Found"] = prepared_df["category_name"].notna().astype(int)

    return prepared_df


def prepare_android_disclosures(
    android_df: pd.DataFrame,
    app_meta_df: pd.DataFrame,
    indicator_columns: list[str],
) -> pd.DataFrame:
    """
    Prepare the Android safety-form export for downstream analysis.
    This helps collapsing repeated app rows and stabilizing indicator fields.
    """

    prepared_df = android_df.copy()
    prepared_df["app_id"] = prepared_df["app_id"].astype(str)
    prepared_df = convert_indicator_columns_to_int(prepared_df, indicator_columns)

    grouped_df = (
        prepared_df.groupby("app_id", dropna = False)
        .agg(
            {
                "Platform": first_non_empty_value,
                "App_Name": first_non_empty_value,
                "Seller": first_non_empty_value,
                "Safety_Forms": first_non_empty_value,
                "URL": first_non_empty_value,
                **{column: "max" for column in indicator_columns},
            }
        )
        .reset_index()
    )

    # Android exports can repeat the same app across rows, so collapse to one disclosure profile per app_id.
    grouped_df["Disclosure Indicator Count"] = grouped_df[indicator_columns].sum(axis = 1)
    grouped_df["Positive Disclosure Columns"] = grouped_df.apply(
        lambda row: build_positive_column_string(row, indicator_columns),
        axis = 1,
    )

    app_meta_prepared = app_meta_df.copy()
    app_meta_prepared["app_id"] = app_meta_prepared["app_id"].astype(str)

    grouped_df = grouped_df.merge(
        app_meta_prepared[
            [
                "app_id",
                "category_name",
                "subcategory_name",
                "cross_store_app_id",
                "initial_release_date",
            ]
        ],
        on = "app_id",
        how = "left",
    )
    grouped_df["Metadata Match Found"] = grouped_df["category_name"].notna().astype(int)

    return grouped_df


def map_ios_disclosures_to_common_labels(
    ios_df: pd.DataFrame,
    abbreviation_map_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Translate iOS disclosure indicators into the shared common-label space.
    This helps cross-platform comparison against harmonized Android disclosures.
    """

    indicator_columns = identify_indicator_columns(ios_df, abbreviation_map_df["Column Name"].tolist())
    # Melt the wide indicator matrix so each positive disclosure becomes one comparable long-format row.
    long_df = ios_df[["app_id", "App_Name", "Seller", "category_name", *indicator_columns]].melt(
        id_vars = ["app_id", "App_Name", "Seller", "category_name"],
        value_vars = indicator_columns,
        var_name = "Source Column",
        value_name = "Indicator Value",
    )
    long_df = long_df[long_df["Indicator Value"] == 1].copy()
    long_df["Platform"] = "iOS"

    return long_df.merge(
        abbreviation_map_df[["Column Name", "Common Label"]],
        left_on = "Source Column",
        right_on = "Column Name",
        how = "left",
    ).drop(columns = ["Column Name"])


def map_android_disclosures_to_common_labels(
    android_df: pd.DataFrame,
    android_taxonomy_map_df: pd.DataFrame,
    translation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Translate Android disclosure indicators into the shared common-label space.
    This helps building a comparable cross-platform label summary.
    """

    indicator_columns = identify_indicator_columns(android_df, android_taxonomy_map_df["Column Name"].tolist())
    # Use the same long-format representation on Android so platform comparison happens on a common schema.
    long_df = android_df[["app_id", "App_Name", "Seller", "category_name", *indicator_columns]].melt(
        id_vars = ["app_id", "App_Name", "Seller", "category_name"],
        value_vars = indicator_columns,
        var_name = "Source Column",
        value_name = "Indicator Value",
    )
    long_df = long_df[long_df["Indicator Value"] == 1].copy()
    long_df["Platform"] = "Android"

    long_df = long_df.merge(
        android_taxonomy_map_df[["Column Name", "Item Name"]],
        left_on = "Source Column",
        right_on = "Column Name",
        how = "left",
    ).drop(columns = ["Column Name"])

    long_df = long_df.merge(
        translation_df[["Item Name", "Common Label"]],
        on = "Item Name",
        how = "left",
    )
    long_df["Common Label"] = long_df["Common Label"].fillna(UNMAPPED_COMMON_LABEL)

    return long_df
