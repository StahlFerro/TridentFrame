import pytest
from pycore.utility.filehandler import read_filesize


@pytest.mark.parametrize("byte_actual, byte_result", [
    (1024, "1 KB"),
    (1023, "1023 B"),
    (512, "512 B"),
    (1200000, "1.144 MB"),
])
def test_read_filesize(byte_actual, byte_result):
    assert read_filesize(byte_actual) == byte_result