import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def scaffold_temp_dir(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("tmp_img")
    return tmp_dir


@pytest.fixture(scope="session")
def fx_path():
    return Path(__file__).resolve().parents[0].joinpath("../_fixtures/")


@pytest.fixture(scope="session")
def fx_sequence_dir(fx_path):
    return fx_path.joinpath("sequence/")


@pytest.fixture(scope="session")
def fx_sequence_dir_contents(fx_sequence_dir):
    return [p for p in fx_sequence_dir.iterdir() if p.stem.startswith("checker_4x4_")]


@pytest.fixture(scope="session")
def fx_checker_apng_path(fx_path):
    return fx_path.joinpath("apng/checker_256px.png")


@pytest.fixture(scope="session")
def fx_json_dir(fx_path):
    return fx_path.joinpath("json/")
