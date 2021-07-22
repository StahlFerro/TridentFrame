import pytest
import shutil
from typing import List
from sys import platform
from pathlib import Path


@pytest.fixture(scope="session")
def scaffold_temp_dir(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("tmp_img")
    return tmp_dir


@pytest.fixture(scope="session")
def scaffold_spaced_dir(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("TridentFrame's Temporary Images")
    return tmp_dir


@pytest.fixture(scope="session")
def fx_spaced_dir_static_image(scaffold_spaced_dir: Path, fx_sequence_dir_contents: List[Path]):
    static_img_path = fx_sequence_dir_contents[0]
    copied_simg = scaffold_spaced_dir.joinpath(static_img_path.name)
    shutil.copy(static_img_path, copied_simg)
    return copied_simg


@pytest.fixture(scope="session")
def fx_spaced_dir_animated_image(scaffold_spaced_dir: Path, fx_checker_apng_path: Path):
    copied_aimg = scaffold_spaced_dir.joinpath(fx_checker_apng_path.name)
    shutil.copy(fx_checker_apng_path, copied_aimg)
    return copied_aimg


@pytest.fixture(scope="session")
def fx_path() -> Path:
    return Path(__file__).resolve().parents[1].joinpath("_fixtures/")


@pytest.fixture(scope="session")
def fx_sequence_dir(fx_path):
    return fx_path.joinpath("sequence/")


@pytest.fixture(scope="session")
def fx_sequence_dir_contents(fx_sequence_dir):
    sequence = [p for p in fx_sequence_dir.iterdir() if p.stem.startswith("checker_4x4_")]
    sequence.sort()
    return sequence


@pytest.fixture(scope="session")
def fx_checker_apng_path(fx_path: Path):
    return fx_path.joinpath("apng/checker_256px.png")


@pytest.fixture(scope="session")
def fx_json_dir(fx_path: Path) -> Path:
    return fx_path.joinpath("json/")


@pytest.fixture(scope="session")
def fx_crbundle_001_create_optimized_gif(fx_json_dir: Path):
    return fx_json_dir.joinpath("crbundle_001_create_optimized_gif.json")


@pytest.fixture(scope="session")
def fx_crbundle_002_create_optimized_apng(fx_json_dir: Path):
    return fx_json_dir.joinpath("crbundle_002_create_optimized_apng.json")


@pytest.fixture(scope="session")
def fx_prod_release_dir():
    return Path(__file__).resolve().parents[2].joinpath("release/tridentframe/")


@pytest.fixture(scope="session")
def fx_prod_unpacked_dir(fx_prod_release_dir):
    os_dirname: str = ""
    if platform.startswith("win"):
        os_dirname = "win-unpacked"
    elif platform.startswith("linux"):
        os_dirname = "linux-unpacked"
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
