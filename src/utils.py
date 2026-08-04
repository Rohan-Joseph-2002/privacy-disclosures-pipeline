"""
AUTHOR: Rohan Joseph
PURPOSE: Provide text-normalization, token-key, indicator-conversion, and console-formatting
         helpers shared by two or more stage scripts, keeping single-use helpers out of this
         module and inside the script that needs them.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-08-04
MODIFIED BY: Rohan Joseph
"""



# ============================================================
# Importing Libraries and Utilities
# ============================================================

import re

import pandas as pd



# ============================================================
# Text Normalization
# ============================================================

def normalize_whitespace(text):
    """
    Normalize repeated whitespace and non-breaking spaces in text.
    This stabilizes the matching and summary output that later stages rely on.
    """

    if not isinstance(text, str):
        return ""

    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_token_key(text):
    """
    Normalize a token-like key by stripping spaces and punctuation while keeping the words.
    This makes joins across column dictionaries and abbreviation maps robust to formatting.
    """

    text = normalize_whitespace(text)
    text = text.replace("\u2019", "'")
    text = text.replace("'", "")
    text = text.replace("-", "")
    text = text.replace(",", "")
    text = text.replace("&", "and")
    text = text.replace("/", "")
    text = text.replace(" ", "")
    text = text.replace(".", "")

    return text.strip()


def compact_path_token(text):
    """
    Compact a path segment into the style used by disclosure indicator column names.
    This reproduces the iOS and Android wide-column naming conventions.
    """

    return normalize_token_key(text)



# ============================================================
# DataFrame Helpers
# ============================================================

def first_non_empty_value(series):
    """
    Return the first non-empty, string-like value from a series.
    This picks a representative value when collapsing repeated app-level rows.
    """

    for value in series.tolist():
        if pd.notna(value):
            cleaned_value = normalize_whitespace(str(value))

            if cleaned_value != "":
                return cleaned_value

    return ""


def convert_indicator_columns_to_int(dataframe, indicator_columns):
    """
    Convert the given indicator columns to deterministic 0/1 integer flags.
    This makes disclosure counts and summaries stable regardless of raw source formatting.
    """

    prepared_dataframe = dataframe.copy()

    if indicator_columns:
        numeric = prepared_dataframe[indicator_columns].apply(pd.to_numeric, errors = "coerce")
        flags = numeric.fillna(0).clip(lower = 0, upper = 1).astype(int)
        prepared_dataframe[indicator_columns] = flags

    return prepared_dataframe


def build_positive_column_string(row, indicator_columns):
    """
    Join the active indicator columns for a row into a stable pipe-delimited string.
    This gives a compact, scannable view of which disclosures a wide row asserts.
    """

    positive_columns = [column for column in indicator_columns if int(row.get(column, 0)) == 1]

    return " | ".join(positive_columns)



# ============================================================
# Console Formatting
# ============================================================

def print_stage_banner(title):
    """
    Print a standardized banner marking the start of a pipeline stage.
    This keeps stage boundaries easy to spot in console output and captured logs.
    """

    rule = "-" * 76
    print(f"\n{rule}\n{title}\n{rule}\n")


def print_section_header(label):
    """
    Print a lightweight section header within a stage run.
    This separates the phases of a stage in the console transcript.
    """

    print(f"\n{label}")


def print_status(message):
    """
    Print a consistently indented status line.
    This makes run logs easier to scan without repeating formatting boilerplate.
    """

    print(f"  > {message}")
