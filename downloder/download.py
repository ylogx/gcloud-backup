import os
import tarfile

from google.cloud import storage
from loguru import logger



class GoogleCloudStorageDownloader(object):
    DEFAULT_LOCAL_DATA_PATH = "data"

    def __init__(self, bucket_name, folder_path, local_download_path=None):
        self.bucket_name = bucket_name
        self.folder_path = folder_path
        self.local_download_path = _validate_local_download_path(local_download_path)

    def download_files(self, gcloud_project=None):
        """Downloads files from a Google Cloud Storage bucket to a local directory"""
        logger.info(f"Downloading files from {self.bucket_name}/{self.folder_path} to {self.local_download_path}")
        storage_client = storage.Client(project=gcloud_project)
        bucket = storage_client.bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=self.folder_path)

        for blob in blobs:
            if not blob.name.endswith("/"):  # ignore directories
                destination_path = os.path.join(self.local_download_path, os.path.relpath(blob.name, self.folder_path))
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                blob.download_to_filename(destination_path)
                logger.debug(f"Downloaded {blob.name} to {destination_path}")

    def compress_files(self, output_filename=None):
        """Compresses the downloaded files into a tar.zst file"""
        import zstandard as zstd

        if output_filename is None:
            output_filename = _pathify(output_filename)
        logger.info(f"Compressing files in {self.local_download_path} to {output_filename}")
        with tarfile.open(output_filename, "w|") as tar:
            tar.add(self.local_download_path, arcname=os.path.basename(self.local_download_path))

        logger.debug(f"Compressed the tar file using zstandard to {output_filename}")
        with open(output_filename, "rb") as tar_file:
            with open(f"{output_filename}.zst", "wb") as zst_file:
                cctx = zstd.ZstdCompressor(level=3)  # Compression level can be adjusted
                cctx.copy_stream(tar_file, zst_file)

        os.remove(output_filename)  # Remove the uncompressed tar file
        logger.debug(f"Compressed to {output_filename}.zst")
        return output_filename


def _pathify(path):
    """Replaces a directory / with a valid filename"""
    if not path:
        return os.getcwd().replace("/", "_") + ".tar.zst"
    output = path.replace("/", "_") + ".tar.zst"
    return output[1:] if output.startswith("_") else output


def _validate_local_download_path(local_download_path=None):
    if local_download_path is None:
        local_download_path = os.path.join(os.getcwd(), GoogleCloudStorageDownloader.DEFAULT_LOCAL_DATA_PATH)
    if not os.path.exists(local_download_path):
        logger.debug(f"Creating directory {local_download_path}")
        os.makedirs(local_download_path)
    return local_download_path
