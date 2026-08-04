"""
AUTHOR: Rohan Joseph
PURPOSE: Prepare the iOS and Android disclosure exports (typed indicators, metadata, row-level
         diagnostics, Android dedup) and map both platforms' positive disclosures into one shared
         common-label space. Shared by the two prepare stages and the harmonization stage.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-08-04
MODIFIED BY: Rohan Joseph
"""



# ============================================================
# Importing Libraries and Utilities
# ============================================================

from src import settings
from src.utils import (
    build_positive_column_string,
    convert_indicator_columns_to_int,
    first_non_empty_value,
)



# ============================================================
# Indicator Preparation
# ============================================================

def identify_indicator_columns(dataframe, candidate_columns):
    """
    Return the candidate indicator columns that are actually present in the dataframe.
    This keeps stage logic robust when a sample export omits some taxonomy columns.
    """

    return [column for column in candidate_columns if column in dataframe.columns]


def attach_metadata(prepared_df, app_meta_df):
    """
    Attach the app metadata columns to a prepared disclosure frame and flag matches.
    This enriches disclosures with cross-store category metadata for later comparison.
    """

    app_meta_prepared = app_meta_df.copy()
    app_meta_prepared["app_id"] = app_meta_prepared["app_id"].astype(str)

    merged_df = prepared_df.merge(
        app_meta_prepared[settings.APP_META_COLUMNS], on = "app_id", how = "left"
    )
    merged_df["Metadata Match Found"] = merged_df["category_name"].notna().astype(int)

    return merged_df


def add_row_diagnostics(prepared_df, indicator_columns):
    """
    Add the per-row disclosure count and positive-column string to a prepared frame.
    This summarizes each app's disclosure profile before metadata is attached.
    """

    prepared_df["Disclosure Indicator Count"] = prepared_df[indicator_columns].sum(axis = 1)
    prepared_df["Positive Disclosure Columns"] = prepared_df.apply(
        lambda row: build_positive_column_string(row, indicator_columns), axis = 1
    )

    return prepared_df


def prepare_ios_disclosures(ios_df, app_meta_df, indicator_columns):
    """
    Prepare the iOS privacy-label export: typed indicators, diagnostics, and app metadata.
    This produces the stable app-level iOS table the harmonization stage maps to common labels.
    """

    prepared_df = ios_df.copy()
    prepared_df["app_id"] = prepared_df["app_id"].astype(str)
    prepared_df = convert_indicator_columns_to_int(prepared_df, indicator_columns)
    prepared_df = add_row_diagnostics(prepared_df, indicator_columns)

    return attach_metadata(prepared_df, app_meta_df)


def prepare_android_disclosures(android_df, app_meta_df, indicator_columns):
    """
    Prepare the Android safety-form export: dedup per app, typed indicators, and metadata.
    This collapses repeated app rows into one disclosure profile before harmonization.
    """

    prepared_df = android_df.copy()
    prepared_df["app_id"] = prepared_df["app_id"].astype(str)
    prepared_df = convert_indicator_columns_to_int(prepared_df, indicator_columns)

    aggregation = {column: first_non_empty_value for column in settings.ANDROID_BASE_COLUMNS[1:]}
    aggregation.update({column: "max" for column in indicator_columns})

    grouped_df = prepared_df.groupby("app_id", dropna = False).agg(aggregation).reset_index()
    grouped_df = add_row_diagnostics(grouped_df, indicator_columns)

    return attach_metadata(grouped_df, app_meta_df)



# ============================================================
# Common-Label Harmonization
# ============================================================

def melt_positive_indicators(disclosures_df, indicator_columns, platform):
    """
    Melt a wide disclosure frame into one long row per positive indicator for a platform.
    This puts both platforms on the same long schema so their labels can be compared.
    """

    id_columns = ["app_id", "App_Name", "Seller", "category_name"]
    long_df = disclosures_df[[*id_columns, *indicator_columns]].melt(
        id_vars = id_columns,
        value_vars = indicator_columns,
        var_name = "Source Column",
        value_name = "Indicator Value",
    )
    long_df = long_df[long_df["Indicator Value"] == 1].copy()
    long_df["Platform"] = platform

    return long_df


def map_ios_disclosures_to_common_labels(ios_df, abbreviation_map_df):
    """
    Translate positive iOS disclosure indicators into the shared common-label space.
    This makes iOS disclosures comparable against harmonized Android disclosures.
    """

    candidate_columns = abbreviation_map_df["Column Name"].tolist()
    indicator_columns = identify_indicator_columns(ios_df, candidate_columns)
    long_df = melt_positive_indicators(ios_df, indicator_columns, "iOS")

    mapped_df = long_df.merge(
        abbreviation_map_df[["Column Name", "Common Label"]],
        left_on = "Source Column",
        right_on = "Column Name",
        how = "left",
    )

    return mapped_df.drop(columns = ["Column Name"])


def map_android_disclosures_to_common_labels(android_df, android_taxonomy_map_df, translation_df):
    """
    Translate positive Android disclosure indicators into the shared common-label space.
    This maps Android columns to item names, then item names to the common label.
    """

    candidate_columns = android_taxonomy_map_df["Column Name"].tolist()
    indicator_columns = identify_indicator_columns(android_df, candidate_columns)
    long_df = melt_positive_indicators(android_df, indicator_columns, "Android")

    long_df = long_df.merge(
        android_taxonomy_map_df[["Column Name", "Item Name"]],
        left_on = "Source Column",
        right_on = "Column Name",
        how = "left",
    ).drop(columns = ["Column Name"])

    long_df = long_df.merge(
        translation_df[["Item Name", "Common Label"]], on = "Item Name", how = "left"
    )
    long_df["Common Label"] = long_df["Common Label"].fillna(settings.UNMAPPED_COMMON_LABEL)

    return long_df
