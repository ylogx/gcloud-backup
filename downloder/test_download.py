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
        ("/tmp/gcd/image/assets/downloder/test1", "test1.tar"),
        ("/tmp/gcd/image/assets/downloder/test/test2", "test2.tar"),
        ("tmp/gcd/image/assets/downloder/test/test3", "test3.tar"),
        ("image/assets/downloder/test/test4", "test4.tar"),
    ],
)
def test_pathify(path, expected):
    assert download._pathify(path) == expected


@pytest.mark.parametrize("path", [None, ""])
def test_pathify_empty(path):
    # Ensure throws assertion error exception
    with pytest.raises(AssertionError):
        download._pathify(path)
