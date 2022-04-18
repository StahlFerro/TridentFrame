import json
import toml
from pathlib import Path

from pycore.core_funcs import config


def test_ensure_settings_not_null():
    assert config.SETTINGS


def test_ensure_temp_dir_exact(fx_dev_root_dir: Path, fx_dev_temp_dir: Path):
    assert fx_dev_root_dir.joinpath(config.TEMP_DIR) == fx_dev_temp_dir


def test_cache_dir_exists(fx_dev_root_dir: Path):
    assert fx_dev_root_dir.joinpath(config.CACHE_DIR).exists()


def test_previews_dir_exists(fx_dev_root_dir: Path):
    assert fx_dev_root_dir.joinpath(config.PREVIEWS_DIR).exists()


def test_engine_config_object_integrity(fx_dev_config_engine_file):
    with open(fx_dev_config_engine_file, "r") as f:
        toml_conf = toml.loads(f.read())
    assert json.dumps(toml_conf) == json.dumps(config.SETTINGS)
    assert toml_conf["cache_dir"] == config.SETTINGS["cache_dir"]
    assert toml_conf["imagers_dir"] == config.SETTINGS["imagers_dir"]
    assert toml_conf["previews_dir"] == config.SETTINGS["previews_dir"]

    assert len(toml_conf["imagers"]["win"]) == len(config.SETTINGS["imagers"]["win"])

    assert toml_conf["imagers"]["win"]["apngopt"] == config.SETTINGS["imagers"]["win"]["apngopt"]
    assert toml_conf["imagers"]["win"]["gifsicle"] == config.SETTINGS["imagers"]["win"]["gifsicle"]
    assert toml_conf["imagers"]["win"]["imagemagick"] == config.SETTINGS["imagers"]["win"]["imagemagick"]
    assert toml_conf["imagers"]["win"]["pngquant"] == config.SETTINGS["imagers"]["win"]["pngquant"]


def test_engine_binaries_exist(fx_dev_bin_dir: Path):
    for platform_name, bins in config.SETTINGS["imagers"].items():
        for bin_name, bin_path in bins.items():
            abs_bin_path = fx_dev_bin_dir.joinpath(platform_name, bin_path)
            assert abs_bin_path.exists()
