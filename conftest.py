from pathlib import Path

import pytest


BASE_DIR = Path(__file__).resolve().parent
TEST_DATA_DIR = BASE_DIR / "tests" / "data"


@pytest.fixture(name="gpx11_str")
def _gpx11_str():
    return TEST_DATA_DIR.joinpath("example-wikipedia.gpx").read_bytes()


@pytest.fixture(name="gpx11")
def _gpx11(gpx11_str):
    from pydantic_gpx.gpx11 import GPX

    return GPX.from_xml(gpx11_str)
