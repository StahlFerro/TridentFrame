import pytest
from pathlib import Path
from pycore.inspect_ops import inspect_static_image, inspect_animated_png
from apng import APNG


TEST_APNG_PATH = Path(__file__).resolve().parents[1].joinpath("_fixtures/apng/checker_256px.png")
TEST_SEQUENCE_PATH = [p for p in Path(__file__).resolve().parents[1].joinpath("_fixtures/sequence/").iterdir()
                 if p.stem.startswith("checker_4x4_")]


def test_inspect_static_image():
    metadata = inspect_static_image(TEST_SEQUENCE_PATH[0])
    assert not metadata.is_animated['value']
    assert metadata.format['value'] == 'PNG'
    assert metadata.width['value'] == 4
    assert metadata.height['value'] == 4


def test_inspect_animated_png():
    apng_im = APNG.open(TEST_APNG_PATH)
    metadata = inspect_animated_png(TEST_APNG_PATH, apng_im)
    assert metadata.is_animated['value']
    assert metadata.delays['value'] == [500 for r in range(0, 4)]
    assert metadata.fps['value'] == 2
    assert metadata.width['value'] == 256
    assert metadata.height['value'] == 256
