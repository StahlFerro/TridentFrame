import pytest
from pathlib import Path
from pycore.inspect_ops import inspect_general, inspect_static_image, inspect_animated_gif, inspect_animated_png
from apng import APNG

#
# TEST_APNG_PATH = Path(__file__).resolve().parents[1].joinpath("_fixtures/apng/checker_256px.png")
# TEST_SEQUENCE_PATH = [p for p in Path(__file__).resolve().parents[1].joinpath("_fixtures/sequence/").iterdir()
#                  if p.stem.startswith("checker_4x4_")]


def test_inspect_static_images(fx_samples_checkers_01_sequence, fx_samples_static_dir_images):
    metadata = inspect_general(fx_samples_checkers_01_sequence[0])
    assert not metadata.is_animated['value']
    assert metadata.format['value'] == 'PNG'
    assert metadata.width['value'] == 4
    assert metadata.height['value'] == 4
    
    for im_path in fx_samples_static_dir_images:
        metadata = inspect_general(im_path)
        assert not metadata.is_animated['value']


def test_inspect_agif(fx_samples_checker_agif_path):
    metadata = inspect_general(fx_samples_checker_agif_path)
    assert metadata.is_animated['value']
    assert metadata.format['value'] == 'GIF'
    assert metadata.delays['value'] == [200 for r in range(0, 4)]
    assert metadata.fps['value'] == 5
    assert metadata.width['value'] == 371
    assert metadata.height['value'] == 371


def test_inspect_apng(fx_samples_checker_apng_path):
    # apng_im = APNG.open(fx_samples_checker_apng_path)
    metadata = inspect_general(fx_samples_checker_apng_path)
    # metadata = inspect_animated_png(fx_samples_checker_apng_path, apng_im)
    assert metadata.is_animated['value']
    assert metadata.format['value'] == 'PNG'
    assert metadata.delays['value'] == [500 for r in range(0, 4)]
    assert metadata.fps['value'] == 2
    assert metadata.width['value'] == 256
    assert metadata.height['value'] == 256
