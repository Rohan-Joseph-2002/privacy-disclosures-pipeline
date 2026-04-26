"""
AUTHOR: Rohan Joseph
PURPOSE: Unit tests for repository environment bootstrapping helpers.
DATE CREATED: 2026-04-26
DATE MODIFIED: 2026-04-26
MODIFIED BY: Codex
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
from pathlib import Path


# --- Import project-specific utilities and pipeline code ---
from scripts.setup_env import ensure_env_file



"""
Functions
"""

def test_ensure_env_file_copies_example_when_env_is_missing(tmp_path: Path) -> None:
    """
    Ensure setup_env creates .env from the tracked template when no local env file exists.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    env_example_path = tmp_path / ".env.example"
    env_example_path.write_text("RUNTIME_MODE=local\nMAX_IOS_ROWS=\n", encoding = "utf-8")

    created_env = ensure_env_file(str(tmp_path))

    assert created_env is True
    assert (tmp_path / ".env").read_text(encoding = "utf-8") == env_example_path.read_text(encoding = "utf-8")


def test_ensure_env_file_does_not_overwrite_existing_env(tmp_path: Path) -> None:
    """
    Ensure setup_env preserves an existing .env file instead of replacing local overrides.
    This helps lock in the expected behavior when the surrounding pipeline changes.
    """

    env_path = tmp_path / ".env"
    env_example_path = tmp_path / ".env.example"

    env_path.write_text("RUNTIME_MODE=custom\n", encoding = "utf-8")
    env_example_path.write_text("RUNTIME_MODE=local\n", encoding = "utf-8")

    created_env = ensure_env_file(str(tmp_path))

    assert created_env is False
    assert env_path.read_text(encoding = "utf-8") == "RUNTIME_MODE=custom\n"
