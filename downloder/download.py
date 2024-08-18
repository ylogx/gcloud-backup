import os
import tarfile

from google.cloud import storage
from loguru import logger
import zstandard as zstd


def download_files_from_gcs(bucket_name, folder_path, local_download_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path)

    if not os.path.exists(local_download_path):
        os.makedirs(local_download_path)

    for blob in blobs:
        if not blob.name.endswith("/"):  # ignore directories
            destination_path = os.path.join(local_download_path, os.path.relpath(blob.name, folder_path))
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            blob.download_to_filename(destination_path)
            logger.debug(f"Downloaded {blob.name} to {destination_path}")


def compress_files_to_zstd_tar(local_download_path, output_filename):
    with tarfile.open(output_filename, "w|") as tar:
        tar.add(local_download_path, arcname=os.path.basename(local_download_path))

    # Compress the tar file using zstandard
    with open(output_filename, "rb") as tar_file:
        with open(f"{output_filename}.zst", "wb") as zst_file:
            cctx = zstd.ZstdCompressor(level=3)  # Compression level can be adjusted
            cctx.copy_stream(tar_file, zst_file)

    os.remove(output_filename)  # Remove the uncompressed tar file
    logger.debug(f"Compressed to {output_filename}.zst")
    return output_filename
