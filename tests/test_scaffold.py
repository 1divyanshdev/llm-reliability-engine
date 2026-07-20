"""Smoke tests for the project scaffold."""

import llm_reliability_engine


def test_package_version() -> None:
    assert llm_reliability_engine.__version__ == "0.1.0"
