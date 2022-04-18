from pathlib import Path


def test_engine_config_file_exists(fx_dev_config_engine_file: Path):
    assert fx_dev_config_engine_file.exists()
