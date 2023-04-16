import pytest
import shutil
import json
from typing import List, Dict
from sys import platform
from pathlib import Path


@pytest.fixture(scope="session")
def scaffold_temp_dir(tmp_path_factory) -> Path:
    tmp_dir = tmp_path_factory.mktemp("tmp_img")
    return tmp_dir


@pytest.fixture(scope="session")
def scaffold_spaced_dir(tmp_path_factory) -> Path:
    tmp_dir = tmp_path_factory.mktemp("TridentFrame's Temporary Images")
    return tmp_dir


# @pytest.fixture()
# def scaffold_spaced_dir(tmp_path) -> Path:
#     full_tmp_path = tmp_path.joinpath("TridentFrame's Temporary Images")
#     full_tmp_path.mkdir()
#     return full_tmp_path


@pytest.fixture(scope="session")
def fx_samples_spaced_dir_static_image(scaffold_spaced_dir: Path, fx_samples_checkers_01_sequence: List[Path]) -> Path:
    static_img_path = fx_samples_checkers_01_sequence[0]
    copied_simg = scaffold_spaced_dir.joinpath(static_img_path.name)
    shutil.copy(static_img_path, copied_simg)
    return copied_simg


@pytest.fixture(scope="session")
def fx_samples_spaced_dir_agif_checker(scaffold_spaced_dir: Path, fx_samples_checker_agif_path: Path):
    copied_aimg = scaffold_spaced_dir.joinpath(fx_samples_checker_agif_path.name)
    shutil.copy(fx_samples_checker_agif_path, copied_aimg)
    return copied_aimg


@pytest.fixture(scope="session")
def fx_samples_spaced_dir_apng_checker(scaffold_spaced_dir: Path, fx_samples_checker_apng_path: Path):
    copied_aimg = scaffold_spaced_dir.joinpath(fx_samples_checker_apng_path.name)
    shutil.copy(fx_samples_checker_apng_path, copied_aimg)
    return copied_aimg


@pytest.fixture(scope="session")
def fx_samples_path() -> Path:
    return Path(__file__).resolve().parents[1].joinpath("_samples/")

@pytest.fixture(scope="session")
def fx_samples_static_dir(fx_samples_path) -> Path:
    return fx_samples_path.joinpath("static/")

@pytest.fixture(scope="session")
def fx_samples_static_dir_images(fx_samples_static_dir: Path) -> List[Path]:
    images = [
        p for p in
        fx_samples_static_dir.iterdir()
        if (p.suffix.lower() == ".png" or p.suffix.lower() == ".gif")
    ]
    images.sort()
    return images


@pytest.fixture(scope="session")
def fx_samples_sequence_dir(fx_samples_path) -> Path:
    return fx_samples_path.joinpath("sequence/")


@pytest.fixture(scope="session")
def fx_samples_checkers_01_dir(fx_samples_path) -> Path:
    return fx_samples_path.joinpath("sequence/tiny_checkers_01/")

@pytest.fixture(scope="session")
def fx_samples_static_01_image(fx_samples_static_dir) -> Path:
    return fx_samples_static_dir.joinpath("static + - = # $ @ & % ,.png")


@pytest.fixture(scope="session")
def fx_samples_checkers_01_sequence(fx_samples_checkers_01_dir) -> List[Path]:
    sequence = [p for p in fx_samples_checkers_01_dir.iterdir() if p.stem.startswith("checker_4x4_")]
    sequence.sort()
    return sequence


@pytest.fixture(scope="session")
def fx_samples_checkers_02_dir(fx_samples_path) -> Path:
    return fx_samples_path.joinpath("sequence/tiny_checkers_02/")


@pytest.fixture(scope="session")
def fx_samples_checkers_02_sequence(fx_samples_checkers_02_dir) -> List[Path]:
    sequence = [p for p in fx_samples_checkers_02_dir.iterdir() if p.stem.startswith("checker_4x4_")]
    sequence.sort()
    return sequence


@pytest.fixture(scope="session")
def fx_samples_disposaltest_dir(fx_samples_path) -> Path:
    return fx_samples_path.joinpath("sequence/disposal_test/")


@pytest.fixture(scope="session")
def fx_samples_disposaltest_sequence(fx_samples_disposaltest_dir) -> List[Path]:
    sequence = [p for p in fx_samples_disposaltest_dir.iterdir() if p.stem.startswith("disposaltest")]
    sequence.sort()
    return sequence


@pytest.fixture(scope="session")
def fx_samples_checker_agif_path(fx_samples_path: Path) -> Path:
    return fx_samples_path.joinpath("agif", "checker_371px.gif")


@pytest.fixture(scope="session")
def fx_samples_checker_apng_path(fx_samples_path: Path) -> Path:
    return fx_samples_path.joinpath("apng", "checker_256px.png")


@pytest.fixture(scope="session")
def fx_samples_json_dir(fx_samples_path: Path) -> Path:
    return fx_samples_path.joinpath("json/")


@pytest.fixture(scope="session")
def fx_samples_crbundle_001_create_optimized_gif_json(fx_samples_json_dir: Path) -> Dict:
    json_path = fx_samples_json_dir.joinpath("crbundle_001_create_optimized_gif.json")
    with open(json_path, "r") as f:
        crpack = json.loads(f.read())
    return crpack


@pytest.fixture(scope="session")
def fx_samples_crbundle_002_create_optimized_apng_json(fx_samples_json_dir: Path) -> Dict:
    json_path = fx_samples_json_dir.joinpath("crbundle_002_create_optimized_apng.json")
    with open(json_path, "r") as f:
        crpack = json.loads(f.read())
    return crpack


@pytest.fixture(scope="session")
def fx_samples_crbundle_004_create_skipped_apng_json(fx_samples_json_dir: Path) -> Dict:
    json_path = fx_samples_json_dir.joinpath("crbundle_004_create_skipped_apng.json")
    with open(json_path, "r") as f:
        crpack = json.loads(f.read())
    return crpack


@pytest.fixture(scope="session")
def fx_samples_splitcriteria_001_split_gif_json(fx_samples_json_dir: Path) -> Dict:
    json_path = fx_samples_json_dir.joinpath("splitcriteria_001_split_gif.json")
    with open(json_path, "r") as f:
        crpack = json.loads(f.read())
    return crpack


@pytest.fixture(scope="session")
def fx_samples_splitcriteria_002_split_gif_json(fx_samples_json_dir: Path) -> Dict:
    json_path = fx_samples_json_dir.joinpath("splitcriteria_002_split_gif.json")
    with open(json_path, "r") as f:
        crpack = json.loads(f.read())
    return crpack


@pytest.fixture(scope="session")
def fx_dev_root_dir():
    return Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def fx_dev_config_dir(fx_dev_root_dir):
    return fx_dev_root_dir.joinpath("config/")


@pytest.fixture(scope="session")
def fx_dev_config_engine_file(fx_dev_config_dir):
    return fx_dev_config_dir.joinpath("engine.toml")


@pytest.fixture(scope="session")
def fx_dev_bin_dir(fx_dev_root_dir):
    return fx_dev_root_dir.joinpath("bin/")


@pytest.fixture(scope="session")
def fx_dev_temp_dir(fx_dev_root_dir):
    return fx_dev_root_dir.joinpath("temp/")


@pytest.fixture(scope="session")
def fx_prod_release_dir():
    return Path(__file__).resolve().parents[2].joinpath("release", "tridentframe/")


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
    return fx_prod_unpacked_dir.joinpath("resources", "app/")


@pytest.fixture(scope="session")
def fx_prod_engine_dir(fx_prod_app_dir):
    engine_subdirname: str = ""
    if platform.startswith("win"):
        engine_subdirname = "windows"
    elif platform.startswith("linux"):
        engine_subdirname = "linux"
    return fx_prod_app_dir.joinpath("engine/", engine_subdirname)


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
def fx_prod_config_engine_file(fx_prod_engine_dir):
    return fx_prod_engine_dir.joinpath("config", "engine.toml")


@pytest.fixture(scope="session")
def fx_prod_exec_path(fx_prod_engine_dir):
    if platform.startswith("win"):
        return fx_prod_engine_dir.joinpath("tridentengine.exe")
    elif platform.startswith("linux"):
        return fx_prod_engine_dir.joinpath("tridentengine")
