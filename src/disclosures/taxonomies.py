"""
AUTHOR: Rohan Joseph
PURPOSE: Taxonomy construction helpers for iOS privacy labels and Android safety forms.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""

from __future__ import annotations



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
from copy import deepcopy

import pandas as pd


# --- Import project-specific utilities and pipeline code ---
from project.settings import (
    ANDROID_DATA_CATEGORIES,
    ANDROID_DATA_PURPOSES,
    ANDROID_DATA_TYPES,
    ANDROID_SAFETY_FORMS_TEMPLATE,
    IOS_DATA_ITEMS,
    IOS_DATA_TYPES,
    IOS_PRIVACY_LABELS_TEMPLATE,
)
from project.utils import compact_path_token, normalize_token_key



"""
Functions
"""

def construct_privacy_labels_dict() -> dict[str, dict[str, dict[str, list[str]]]]:
    """
    Construct the iOS privacy-label taxonomy dictionary.
    This helps keep the taxonomy definition reproducible within the repository.
    """

    privacy_labels = deepcopy(IOS_PRIVACY_LABELS_TEMPLATE)

    for privacy_label in ["Data Linked to You", "Data Not Linked to You"]:
        for data_use in privacy_labels[privacy_label].keys():
            for data_type in IOS_DATA_TYPES:
                privacy_labels[privacy_label][data_use][data_type] = IOS_DATA_ITEMS[data_type]

    return privacy_labels


def build_privacy_labels_map(privacy_labels_dict: dict[str, dict[str, dict[str, list[str]]]]) -> pd.DataFrame:
    """
    Build the iOS privacy-label taxonomy map.
    This helps reproduce the wide-column indicator structure used in the raw export.
    """

    rows: list[dict[str, object]] = []

    for privacy_label, second_layer in privacy_labels_dict.items():
        if privacy_label == "Data Used to Track You":
            for data_type in IOS_DATA_TYPES:
                for data_item in IOS_DATA_ITEMS[data_type]:
                    rows.append(
                        {
                            "Column Name": "_".join(
                                [
                                    compact_path_token(privacy_label),
                                    compact_path_token(data_type),
                                    compact_path_token(data_item),
                                ]
                            ),
                            "Element": f"{privacy_label} -> {data_type} -> {data_item}",
                            "Privacy Label": privacy_label,
                            "Data Use": "",
                            "Data Type": data_type,
                            "Data Item": data_item,
                        }
                    )
        else:
            for data_use, data_types_dict in second_layer.items():
                for data_type, data_items_list in data_types_dict.items():
                    for data_item in data_items_list:
                        rows.append(
                            {
                                "Column Name": "_".join(
                                    [
                                        compact_path_token(privacy_label),
                                        compact_path_token(data_use),
                                        compact_path_token(data_type),
                                        compact_path_token(data_item),
                                    ]
                                ),
                                "Element": f"{privacy_label} -> {data_use} -> {data_type} -> {data_item}",
                                "Privacy Label": privacy_label,
                                "Data Use": data_use,
                                "Data Type": data_type,
                                "Data Item": data_item,
                            }
                        )

    return pd.DataFrame(rows)


def construct_safety_forms_dict() -> dict[str, dict[str, dict[str, list[str]]]]:
    """
    Construct the Android safety-form taxonomy dictionary.
    This helps reproduce the raw disclosure hierarchy inside the repository.
    """

    safety_forms = deepcopy(ANDROID_SAFETY_FORMS_TEMPLATE)

    for safety_form in ["Data shared", "Data collected"]:
        for data_category in ANDROID_DATA_CATEGORIES:
            safety_forms[safety_form][data_category] = {}
            for data_type in ANDROID_DATA_TYPES[data_category].keys():
                safety_forms[safety_form][data_category][data_type] = ANDROID_DATA_PURPOSES

    safety_forms["Security practices"] = {
        "Security practices": safety_forms["Security practices"]
    }

    return safety_forms


def build_safety_forms_map(safety_forms_dict: dict[str, dict[str, dict[str, list[str]]]]) -> pd.DataFrame:
    """
    Build the Android safety-form taxonomy map.
    This helps translating raw wide-column indicators into explicit path metadata.
    """

    rows: list[dict[str, object]] = []

    for safety_form, categories_dict in safety_forms_dict.items():
        if safety_form == "Security practices":
            for security_practice in categories_dict["Security practices"]:
                rows.append(
                    {
                        "Column Name": "_".join(
                            [
                                compact_path_token(safety_form),
                                compact_path_token(security_practice),
                            ]
                        ),
                        "Item Name": security_practice,
                        "Element": f"{safety_form} -> {security_practice}",
                        "Safety Form": safety_form,
                        "Security Practice": security_practice,
                        "Data Category": "",
                        "Data Type": "",
                        "Data Purpose": "",
                    }
                )
        else:
            for data_category, data_types_dict in categories_dict.items():
                for data_type, data_purposes_list in data_types_dict.items():
                    for data_purpose in data_purposes_list:
                        rows.append(
                            {
                                "Column Name": "_".join(
                                    [
                                        compact_path_token(safety_form),
                                        compact_path_token(data_category),
                                        compact_path_token(data_type),
                                        compact_path_token(data_purpose),
                                    ]
                                ),
                                "Item Name": "_".join([safety_form, data_category, data_type, data_purpose]),
                                "Element": f"{safety_form} -> {data_category} -> {data_type} -> {data_purpose}",
                                "Safety Form": safety_form,
                                "Security Practice": "",
                                "Data Category": data_category,
                                "Data Type": data_type,
                                "Data Purpose": data_purpose,
                            }
                        )

    rows.append(
        {
            "Column Name": "Nodatasharedwiththirdparties",
            "Item Name": "No data shared with third parties",
            "Element": "No data shared with third parties",
            "Safety Form": "",
            "Security Practice": "",
            "Data Category": "",
            "Data Type": "",
            "Data Purpose": "",
        }
    )
    rows.append(
        {
            "Column Name": "Nodatacollected",
            "Item Name": "No data collected",
            "Element": "No data collected",
            "Safety Form": "",
            "Security Practice": "",
            "Data Category": "",
            "Data Type": "",
            "Data Purpose": "",
        }
    )

    return pd.DataFrame(rows)


def prepare_privacy_label_abbreviation_map(abbreviation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the privacy-label abbreviation map used for common-label harmonization.
    This helps translating iOS indicator columns into the shared label space.
    """

    prepared_df = abbreviation_df.copy()
    prepared_df = prepared_df.iloc[:, :2].copy()
    prepared_df.columns = ["Source Term", "Common Label"]
    prepared_df = prepared_df.dropna(subset = ["Source Term", "Common Label"]).reset_index(drop = True)
    prepared_df["Column Name"] = prepared_df["Source Term"].apply(
        lambda value: "_".join(compact_path_token(segment) for segment in str(value).split("_"))
    )
    prepared_df["Normalized Source Term"] = prepared_df["Source Term"].astype(str).apply(normalize_token_key)

    return prepared_df


def prepare_android_to_ios_translation_map(translation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the Android-to-iOS translation table used for common-label harmonization.
    This helps translating Android disclosure paths into the shared label space.
    """

    prepared_df = translation_df.copy()
    prepared_df = prepared_df[["item_name", "lab1", "lab2", "lab3", "lab4", "label"]].copy()
    prepared_df.columns = ["Item Name", "Lab 1", "Lab 2", "Lab 3", "Lab 4", "Common Label"]
    prepared_df["Normalized Item Name"] = prepared_df["Item Name"].astype(str).apply(normalize_token_key)

    return prepared_df


def build_platform_registry_summary(log_sheet_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a compact summary of the platform registry sheet.
    This helps documenting what the bundled sample log sheet contains.
    """

    rows = []

    for column in log_sheet_df.columns:
        rows.append(
            {
                "Registry Column": column,
                "Non-Null Count": int(log_sheet_df[column].notna().sum()),
            }
        )

    return pd.DataFrame(rows)
