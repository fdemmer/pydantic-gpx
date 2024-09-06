from pathlib import Path

import pytest


BASE_DIR = Path(__file__).resolve().parent
TEST_DATA_DIR = BASE_DIR / "tests" / "data"


@pytest.fixture()
def example_wikipedia_gpx():
    return TEST_DATA_DIR.joinpath("example-wikipedia.gpx").read_bytes()


@pytest.fixture()
def gpx11_with_all_fields():
    return TEST_DATA_DIR.joinpath("gpx1.1_with_all_fields.gpx").read_bytes()


@pytest.fixture()
def gpx11_large():
    return TEST_DATA_DIR.joinpath("1C07C8B25CCE4CC17DED39F37936AA15.gpx").read_bytes()


@pytest.fixture()
def gpx11(gpx11_with_all_fields):
    from pydantic_gpx.gpx11 import GPX

    return GPX.from_xml(gpx11_with_all_fields)


@pytest.fixture()
def gpxpy_examples():
    return Path("/home/florian/Code/other/gpxpy/test_files").glob("*.gpx")
