import os
import pytest

from downloder import download

cwd = os.getcwd()


@pytest.mark.parametrize(
    "path, expected",
    [
        (None, cwd + "/test_path"),
        ("/tmp/gcd/User/Documents/downloder/test", "/tmp/gcd/User/Documents/downloder/test"),
        ("/tmp/gcd/User/Documents/downloder/test/test", "/tmp/gcd/User/Documents/downloder/test/test"),
    ],
)
def test_validate_local_download_path(path, expected):
    downloader = download.GoogleCloudStorageDownloader(
        bucket_name="bucket_name", folder_path="folder/test_path", local_download_path=path
    )
    downloader._validate_local_download_path()
    assert downloader.local_download_path == expected
    assert os.path.exists(expected)


@pytest.mark.parametrize(
    "path, expected",
    [
        ("/tmp/gcd/User/Documents/downloder/test", "tmp_gcd_User_Documents_downloder_test.tar"),
        ("/tmp/gcd/User/Documents/downloder/test/test", "tmp_gcd_User_Documents_downloder_test_test.tar"),
        ("tmp/gcd/User/Documents/downloder/test/test", "tmp_gcd_User_Documents_downloder_test_test.tar"),
        ("User/Documents/downloder/test/test", "User_Documents_downloder_test_test.tar"),
    ],
)
def test_pathify(path, expected):
    assert download._pathify(path) == expected


def test_pathify_empty():
    assert download._pathify(path="") == cwd.replace("/", "_") + ".tar"
