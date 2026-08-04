"""
AUTHOR: Rohan Joseph
PURPOSE: Reconstruct the iOS privacy-label and Android safety-form taxonomies inside the repo and
         build their wide-column maps, plus prepare the abbreviation and Android-to-iOS translation
         reference tables used for cross-platform harmonization.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-08-04
MODIFIED BY: Rohan Joseph
"""



# ============================================================
# Importing Libraries and Utilities
# ============================================================

import pandas as pd

from copy import deepcopy

from src import settings
from src.utils import compact_path_token, normalize_token_key



# ============================================================
# Join Helpers
# ============================================================

def compact_join(*parts):
    """
    Join path segments into the compact underscore column-name style.
    This reproduces the wide-column indicator names used in the raw disclosure exports.
    """

    return "_".join(compact_path_token(part) for part in parts)


def arrow_join(*parts):
    """
    Join path segments with the arrow separator used in the human-readable Element column.
    This keeps the taxonomy map's readable path consistent across builders.
    """

    return " -> ".join(parts)


def recompact_column_name(value):
    """
    Re-compact an underscore-delimited source term into the canonical column-name form.
    This aligns abbreviation-map keys with the taxonomy map's Column Name values.
    """

    return "_".join(compact_path_token(segment) for segment in str(value).split("_"))



# ============================================================
# iOS Taxonomy
# ============================================================

def construct_privacy_labels_dict():
    """
    Construct the nested iOS privacy-label taxonomy dictionary from the templates.
    This keeps the taxonomy definition reproducible within the repository.
    """

    privacy_labels = deepcopy(settings.IOS_PRIVACY_LABELS_TEMPLATE)

    for privacy_label in ["Data Linked to You", "Data Not Linked to You"]:
        for data_use in privacy_labels[privacy_label]:
            for data_type in settings.IOS_DATA_TYPES:
                data_items = settings.IOS_DATA_ITEMS[data_type]
                privacy_labels[privacy_label][data_use][data_type] = data_items

    return privacy_labels


def build_track_row(privacy_label, data_type, data_item):
    """
    Build one taxonomy-map row for a "Data Used to Track You" indicator (no data-use layer).
    This keeps the track branch of the iOS map builder compact.
    """

    return {
        "Column Name": compact_join(privacy_label, data_type, data_item),
        "Element": arrow_join(privacy_label, data_type, data_item),
        "Privacy Label": privacy_label,
        "Data Use": "",
        "Data Type": data_type,
        "Data Item": data_item,
    }


def build_linked_row(privacy_label, data_use, data_type, data_item):
    """
    Build one taxonomy-map row for a linked/not-linked indicator with a data-use layer.
    This keeps the linked branch of the iOS map builder compact.
    """

    return {
        "Column Name": compact_join(privacy_label, data_use, data_type, data_item),
        "Element": arrow_join(privacy_label, data_use, data_type, data_item),
        "Privacy Label": privacy_label,
        "Data Use": data_use,
        "Data Type": data_type,
        "Data Item": data_item,
    }


def build_privacy_labels_map(privacy_labels_dict):
    """
    Build the flat iOS privacy-label taxonomy map with one row per indicator column.
    This reproduces the wide-column indicator structure the raw export uses.
    """

    rows = []

    for privacy_label, second_layer in privacy_labels_dict.items():
        if privacy_label == "Data Used to Track You":
            for data_type in settings.IOS_DATA_TYPES:
                for data_item in settings.IOS_DATA_ITEMS[data_type]:
                    rows.append(build_track_row(privacy_label, data_type, data_item))
            continue

        for data_use, data_types_dict in second_layer.items():
            for data_type, data_items_list in data_types_dict.items():
                for data_item in data_items_list:
                    rows.append(build_linked_row(privacy_label, data_use, data_type, data_item))

    return pd.DataFrame(rows)



# ============================================================
# Android Taxonomy
# ============================================================

def construct_safety_forms_dict():
    """
    Construct the nested Android safety-form taxonomy dictionary from the templates.
    This reproduces the raw disclosure hierarchy inside the repository.
    """

    safety_forms = deepcopy(settings.ANDROID_SAFETY_FORMS_TEMPLATE)

    for safety_form in ["Data shared", "Data collected"]:
        for data_category in settings.ANDROID_DATA_CATEGORIES:
            safety_forms[safety_form][data_category] = {}

            for data_type in settings.ANDROID_DATA_TYPES[data_category]:
                safety_forms[safety_form][data_category][data_type] = settings.ANDROID_DATA_PURPOSES

    safety_forms["Security practices"] = {"Security practices": safety_forms["Security practices"]}

    return safety_forms


def build_security_practice_row(safety_form, security_practice):
    """
    Build one taxonomy-map row for an Android security-practice item.
    This keeps the security-practice branch of the map builder compact.
    """

    return {
        "Column Name": compact_join(safety_form, security_practice),
        "Item Name": security_practice,
        "Element": arrow_join(safety_form, security_practice),
        "Safety Form": safety_form,
        "Security Practice": security_practice,
        "Data Category": "",
        "Data Type": "",
        "Data Purpose": "",
    }


def build_data_path_row(safety_form, data_category, data_type, data_purpose):
    """
    Build one taxonomy-map row for an Android data collection/sharing path.
    This keeps the data-path branch of the map builder compact.
    """

    item_name = "_".join([safety_form, data_category, data_type, data_purpose])

    return {
        "Column Name": compact_join(safety_form, data_category, data_type, data_purpose),
        "Item Name": item_name,
        "Element": arrow_join(safety_form, data_category, data_type, data_purpose),
        "Safety Form": safety_form,
        "Security Practice": "",
        "Data Category": data_category,
        "Data Type": data_type,
        "Data Purpose": data_purpose,
    }


def status_row(column_name, item_name):
    """
    Build one taxonomy-map row for an Android status column with empty path fields.
    This appends the "no data" status columns to the Android map.
    """

    return {
        "Column Name": column_name,
        "Item Name": item_name,
        "Element": item_name,
        "Safety Form": "",
        "Security Practice": "",
        "Data Category": "",
        "Data Type": "",
        "Data Purpose": "",
    }


def build_safety_forms_map(safety_forms_dict):
    """
    Build the flat Android safety-form taxonomy map with one row per indicator column.
    This translates the raw wide-column indicators into explicit path metadata.
    """

    rows = []

    for safety_form, categories_dict in safety_forms_dict.items():
        if safety_form == "Security practices":
            for security_practice in categories_dict["Security practices"]:
                rows.append(build_security_practice_row(safety_form, security_practice))
            continue

        for data_category, data_types_dict in categories_dict.items():
            for data_type, data_purposes_list in data_types_dict.items():
                for data_purpose in data_purposes_list:
                    rows.append(
                        build_data_path_row(safety_form, data_category, data_type, data_purpose)
                    )

    rows.append(status_row("Nodatasharedwiththirdparties", "No data shared with third parties"))
    rows.append(status_row("Nodatacollected", "No data collected"))

    return pd.DataFrame(rows)



# ============================================================
# Reference Maps
# ============================================================

def prepare_privacy_label_abbreviation_map(abbreviation_df):
    """
    Prepare the iOS abbreviation map (source term to common label) used for harmonization.
    This translates iOS indicator columns into the shared common-label space.
    """

    prepared_df = abbreviation_df.iloc[:, :2].copy()
    prepared_df.columns = ["Source Term", "Common Label"]
    prepared_df = prepared_df.dropna(subset = ["Source Term", "Common Label"])
    prepared_df = prepared_df.reset_index(drop = True)
    prepared_df["Column Name"] = prepared_df["Source Term"].apply(recompact_column_name)
    source_terms = prepared_df["Source Term"].astype(str)
    prepared_df["Normalized Source Term"] = source_terms.apply(normalize_token_key)

    return prepared_df


def prepare_android_to_ios_translation_map(translation_df):
    """
    Prepare the Android-to-iOS translation table used for common-label harmonization.
    This translates Android disclosure paths into the shared common-label space.
    """

    columns = ["item_name", "lab1", "lab2", "lab3", "lab4", "label"]
    prepared_df = translation_df[columns].copy()
    prepared_df.columns = ["Item Name", "Lab 1", "Lab 2", "Lab 3", "Lab 4", "Common Label"]
    item_names = prepared_df["Item Name"].astype(str)
    prepared_df["Normalized Item Name"] = item_names.apply(normalize_token_key)

    return prepared_df


def build_platform_registry_summary(log_sheet_df):
    """
    Build a compact non-null count summary of the platform registry log sheet.
    This documents what the bundled sample log sheet actually contains.
    """

    rows = []

    for column in log_sheet_df.columns:
        non_null_count = int(log_sheet_df[column].notna().sum())
        rows.append({"Registry Column": column, "Non-Null Count": non_null_count})

    return pd.DataFrame(rows)
