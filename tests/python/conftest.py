import pytest
from sys import platform
from pathlib import Path


@pytest.fixture(scope="session")
def scaffold_temp_dir(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("tmp_img")
    return tmp_dir


@pytest.fixture(scope="session")
def fx_path():
    return Path(__file__).resolve().parents[1].joinpath("_fixtures/")


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


@pytest.fixture(scope="session")
def fx_prod_release_dir():
    return Path(__file__).resolve().parents[2].joinpath("release/tridentframe/")


@pytest.fixture(scope="session")
def fx_prod_unpacked_dir(fx_prod_release_dir):
    os_dirname: str = ""
    if platform.startswith("win"):
        os_dirname = "win-unpacked"
    elif platform.startswith("linux"):
        os_dirname = "linux"
    return fx_prod_release_dir.joinpath(os_dirname)


@pytest.fixture(scope="session")
def fx_prod_app_dir(fx_prod_unpacked_dir):
    return fx_prod_unpacked_dir.joinpath("resources/app/")


@pytest.fixture(scope="session")
def fx_prod_engine_dir(fx_prod_app_dir):
    engine_dirname: str = ""
    if platform.startswith("win"):
        engine_dirname = "windows"
    elif platform.startswith("linux"):
        engine_dirname = "linux"
    return fx_prod_app_dir.joinpath("engine/", engine_dirname)


@pytest.fixture(scope="session")
def fx_prod_temp_dir(fx_prod_engine_dir):
    return fx_prod_engine_dir.joinpath("temp/")


@pytest.fixture(scope="session")
def fx_prod_cache_dir(fx_prod_temp_dir):
    return fx_prod_temp_dir.joinpath("cache/")


@pytest.fixture(scope="session")
def fx_prod_previews_dir(fx_prod_temp_dir):
    return fx_prod_temp_dir.joinpath("previews/")


@pytest.fixture(scope="session")
def fx_prod_imagers_jsonpath(fx_prod_engine_dir):
    return fx_prod_engine_dir.joinpath("config/imagers.json")


@pytest.fixture(scope="session")
def fx_prod_settings_jsonpath(fx_prod_engine_dir):
    return fx_prod_engine_dir.joinpath("config/settings.json")


@pytest.fixture(scope="session")
def fx_prod_exec_path(fx_prod_engine_dir):
    if platform.startswith("win"):
        return fx_prod_engine_dir.joinpath("tridentengine.exe")
    elif platform.startswith("linux"):
        return fx_prod_engine_dir.joinpath("tridentengine")
