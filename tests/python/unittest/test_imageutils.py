import pytest
from pycore.utility.imageutils import shout_indices


@pytest.mark.parametrize("frame_count, percentage_mult, percentage_expected", [
    (24, 50, {0: "0%", 12: "50%"}),
    (40, 25, {0: "0%", 10: "25%", 20: "50%", 30: "75%"})
])
def test_shout_indices(frame_count, percentage_mult, percentage_expected):
    assert shout_indices(frame_count, percentage_mult) == percentage_expected

