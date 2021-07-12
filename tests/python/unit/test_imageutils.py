import pytest
from pathlib import Path
from pycore.utility.imageutils import shout_indices, png_is_animated, get_image_delays, shift_image_sequence \
    , sequence_nameget


TEST_APNG_PATH = Path(__file__).resolve().parents[1].joinpath("_fixtures/apng/checker_256px.png")
TEST_SEQUENCE_PATH = [p for p in Path(__file__).resolve().parents[1].joinpath("_fixtures/sequence/").iterdir()
                 if p.stem.startswith("checker_4x4_")]


@pytest.mark.parametrize("frame_count, percentage_mult, percentage_expected", [
    (24, 50, {0: "0%", 12: "50%"}),
    (40, 25, {0: "0%", 10: "25%", 20: "50%", 30: "75%"})
])
def test_shout_indices(frame_count, percentage_mult, percentage_expected):
    assert shout_indices(frame_count, percentage_mult) == percentage_expected


def test_png_is_animated():
    assert png_is_animated(TEST_APNG_PATH)


def test_get_image_delays():
    assert list(get_image_delays(TEST_APNG_PATH, "PNG")) == [500 for r in range(0, 4)]


@pytest.mark.parametrize("shift_number, expected_list", [
    (2, ["checker_4x4_00002.png", "checker_4x4_00003.png", "checker_4x4_00000.png", "checker_4x4_00001.png"]),
    (-1, ["checker_4x4_00003.png", "checker_4x4_00000.png", "checker_4x4_00001.png", "checker_4x4_00002.png"])
])
def test_shift_image_sequence(shift_number, expected_list):
    shifted_fnames = [sp.name for sp in shift_image_sequence(TEST_SEQUENCE_PATH, shift_number)]
    assert shifted_fnames == expected_list


@pytest.mark.parametrize("image, sequenceless_name", [
    (TEST_SEQUENCE_PATH[0].name, "checker_4x4"),
    (TEST_SEQUENCE_PATH[1], "checker_4x4"),
    (TEST_SEQUENCE_PATH[2], "checker_4x4"),
    (TEST_SEQUENCE_PATH[3].name, "checker_4x4"),
    (Path("argon_winder_000420.tar.gz").resolve(), "argon_winder"),
])
def test_sequence_nameget(image, sequenceless_name):
    assert sequence_nameget(image) == sequenceless_name
