import pytest
from pathlib import Path
from pycore.utility.imageutils import shout_indices, png_is_animated, get_image_delays, shift_image_sequence \
    , sequence_nameget


# TEST_APNG_PATH = Path(__file__).resolve().parents[1].joinpath("_fixtures/apng/checker_256px.png")
# TEST_SEQUENCE_PATH = [p for p in Path(__file__).resolve().parents[1].joinpath("_fixtures/sequence/").iterdir()
#                  if p.stem.startswith("checker_4x4_")]


@pytest.mark.parametrize("frame_count, percentage_mult, percentage_expected", [
    (24, 50, {0: "0%", 12: "50%"}),
    (40, 25, {0: "0%", 10: "25%", 20: "50%", 30: "75%"})
])
def test_shout_indices(frame_count, percentage_mult, percentage_expected):
    assert shout_indices(frame_count, percentage_mult) == percentage_expected


def test_png_is_animated(fx_checker_apng_path):
    assert png_is_animated(fx_checker_apng_path)


def test_get_image_delays(fx_checker_apng_path):
    assert list(get_image_delays(fx_checker_apng_path, "PNG")) == [500 for r in range(0, 4)]


@pytest.mark.parametrize("shift_number, expected_list", [
    (2, ["checker_4x4_00002.png", "checker_4x4_00003.png", "checker_4x4_00000.png", "checker_4x4_00001.png"]),
    (-1, ["checker_4x4_00003.png", "checker_4x4_00000.png", "checker_4x4_00001.png", "checker_4x4_00002.png"])
])
def test_shift_image_sequence(shift_number, expected_list, fx_sequence_dir_contents):
    shifted_fnames = [sp.name for sp in shift_image_sequence(fx_sequence_dir_contents, shift_number)]
    assert shifted_fnames == expected_list


def test_actual_sequence_nameget(fx_sequence_dir_contents):
    for fpath in fx_sequence_dir_contents:
        assert sequence_nameget(fpath.name) == "checker_4x4"


def test_fake_file_sequence_nameget():
    fake_file = Path("argon_winder_000420.tar.gz").resolve()
    assert sequence_nameget(fake_file) == "argon_winder"
