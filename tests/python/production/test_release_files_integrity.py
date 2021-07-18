from pathlib import Path


def test_temp_dir_exists(fx_prod_temp_dir: Path):
    assert fx_prod_temp_dir.exists()


def test_cache_dir_exists(fx_prod_cache_dir: Path):
    assert fx_prod_cache_dir.exists()


def test_previews_dir_exists(fx_prod_previews_dir: Path):
    assert fx_prod_previews_dir.exists()


def test_imagers_jsonfile_exists(fx_prod_imagers_jsonpath: Path):
    assert fx_prod_imagers_jsonpath.exists()


def test_settings_jsonfile_exists(fx_prod_settings_jsonpath: Path):
    assert fx_prod_settings_jsonpath.exists()


def test_exec_exists(fx_prod_exec_path: Path):
    assert fx_prod_exec_path.exists()
