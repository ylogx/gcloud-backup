import os
import pytest

from downloder import download

cwd = os.getcwd()


@pytest.mark.parametrize(
    "path, expected",
    [
        (None, cwd + "/data"),
        ("/tmp/gcd/User/Documents/downloder/test", "/tmp/gcd/User/Documents/downloder/test"),
        ("/tmp/gcd/User/Documents/downloder/test/test", "/tmp/gcd/User/Documents/downloder/test/test"),
    ],
)
def test_validate_local_download_path(path, expected):
    assert download.validate_local_download_path(local_download_path=path) == expected
    assert os.path.exists(expected)


@pytest.mark.parametrize(
    "path, expected",
    [
        ("/tmp/gcd/User/Documents/downloder/test", "tmp_gcd_User_Documents_downloder_test.tar.zst"),
        ("/tmp/gcd/User/Documents/downloder/test/test", "tmp_gcd_User_Documents_downloder_test_test.tar.zst"),
        ("tmp/gcd/User/Documents/downloder/test/test", "tmp_gcd_User_Documents_downloder_test_test.tar.zst"),
        ("User/Documents/downloder/test/test", "User_Documents_downloder_test_test.tar.zst"),
    ],
)
def test_pathify(path, expected):
    assert download.pathify(path) == expected


def test_pathify_empty():
    assert download.pathify(path="") == cwd.replace("/", "_") + ".tar.zst"
