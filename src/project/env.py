"""
AUTHOR: Rohan Joseph
PURPOSE: Environment loading and runtime configuration validation.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""

from __future__ import annotations



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import os

from dataclasses import dataclass


# --- Import project-specific utilities and pipeline code ---
from project.paths import PROJECT_ROOT
from project.settings import DEFAULT_MAX_ANDROID_ROWS, DEFAULT_MAX_IOS_ROWS



"""
Settings
"""

ENV_FILE = os.path.join(PROJECT_ROOT, ".env")
DEFAULT_IOS_PRIVACY_LABELS_PATH = os.path.join("input", "ios_privacy_labels_sample", "ios_privacy_labels_sample.csv")
DEFAULT_ANDROID_SAFETY_FORMS_PATH = os.path.join("input", "android_safety_forms_sample", "android_safety_forms_sample.csv")
DEFAULT_ANDROID_TO_IOS_MAP_PATH = os.path.join("input", "reference", "android_to_ios_taxonomy_map_sample.csv")
DEFAULT_PRIVACY_LABEL_ABBREVIATIONS_PATH = os.path.join("input", "reference", "privacy_label_term_abbr_sample.xlsx")
DEFAULT_APP_META_PATH = os.path.join("input", "reference", "app_meta_sample.csv")
DEFAULT_APP_LOG_SHEET_PATH = os.path.join("input", "reference", "app_log_sheet_sample.csv")



"""
Classes
"""

@dataclass(frozen = True)
class RuntimeConfig:
    """
    Typed runtime configuration for the repository.
    This gives the rest of the repository one typed source of runtime settings and paths.
    """

    runtime_mode: str
    ios_privacy_labels_path: str
    android_safety_forms_path: str
    android_to_ios_map_path: str
    privacy_label_abbreviations_path: str
    app_meta_path: str
    app_log_sheet_path: str
    max_ios_rows: int
    max_android_rows: int



"""
Functions
"""

def load_dotenv_file(env_path: str = ENV_FILE) -> None:
    """
    Load key-value pairs from a local .env file into the process environment.
    This helps keep the repository self-contained without requiring external dotenv packages.
    """

    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding = "utf-8") as handle:
        raw_lines = handle.readlines()

    for raw_line in raw_lines:
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if key and key not in os.environ:
            # Respect any variables the caller already supplied while still honoring repo-local defaults.
            os.environ[key] = value


def resolve_project_path(path_value: str | None, default_path: str) -> str:
    """
    Resolve a configured path relative to the project root when needed.
    This helps support portable local defaults without forcing absolute paths in .env files.
    """

    if path_value is None or path_value == "":
        # Fall back to the bundled sample path when no override is provided.
        return os.path.abspath(os.path.join(PROJECT_ROOT, default_path))

    candidate_path = os.path.expanduser(path_value)

    if os.path.isabs(candidate_path):
        return os.path.abspath(candidate_path)

    return os.path.abspath(os.path.join(PROJECT_ROOT, candidate_path))


def resolve_optional_int(value: str | None, default_value: int) -> int:
    """
    Resolve an optional integer environment variable.
    This helps keep row-limiting configuration simple.
    """

    if value is None or value == "":
        return default_value

    return int(value)


def get_runtime_config() -> RuntimeConfig:
    """
    Build the runtime configuration from environment variables and .env.
    This helps standardize path handling and stage behavior across entry scripts.
    """

    load_dotenv_file()

    # Assemble one typed config object so every script resolves paths and thresholds the same way.
    return RuntimeConfig(
        runtime_mode = os.environ.get("RUNTIME_MODE", "local"),
        ios_privacy_labels_path = resolve_project_path(
            path_value = os.environ.get("IOS_PRIVACY_LABELS_PATH"),
            default_path = DEFAULT_IOS_PRIVACY_LABELS_PATH,
        ),
        android_safety_forms_path = resolve_project_path(
            path_value = os.environ.get("ANDROID_SAFETY_FORMS_PATH"),
            default_path = DEFAULT_ANDROID_SAFETY_FORMS_PATH,
        ),
        android_to_ios_map_path = resolve_project_path(
            path_value = os.environ.get("ANDROID_TO_IOS_MAP_PATH"),
            default_path = DEFAULT_ANDROID_TO_IOS_MAP_PATH,
        ),
        privacy_label_abbreviations_path = resolve_project_path(
            path_value = os.environ.get("PRIVACY_LABEL_ABBREVIATIONS_PATH"),
            default_path = DEFAULT_PRIVACY_LABEL_ABBREVIATIONS_PATH,
        ),
        app_meta_path = resolve_project_path(
            path_value = os.environ.get("APP_META_PATH"),
            default_path = DEFAULT_APP_META_PATH,
        ),
        app_log_sheet_path = resolve_project_path(
            path_value = os.environ.get("APP_LOG_SHEET_PATH"),
            default_path = DEFAULT_APP_LOG_SHEET_PATH,
        ),
        max_ios_rows = resolve_optional_int(os.environ.get("MAX_IOS_ROWS"), DEFAULT_MAX_IOS_ROWS),
        max_android_rows = resolve_optional_int(os.environ.get("MAX_ANDROID_ROWS"), DEFAULT_MAX_ANDROID_ROWS),
    )
