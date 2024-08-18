import os
import tarfile

from google.cloud import storage
from loguru import logger
import tqdm
import zstandard as zstd

DEFAULT_LOCAL_DATA_PATH = "data"


def download_files_from_gcs(bucket_name, folder_path, local_download_path=None):
    local_download_path = validate_local_download_path(local_download_path)
    logger.debug(f"Downloading files from {bucket_name}/{folder_path} to {local_download_path}")

    storage_client = storage.Client(project="lineage-sc")
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path)

    for blob in blobs:
        if not blob.name.endswith("/"):  # ignore directories
            destination_path = os.path.join(local_download_path, os.path.relpath(blob.name, folder_path))
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            blob.download_to_filename(destination_path)
            logger.debug(f"Downloaded {blob.name} to {destination_path}")


def compress_files_to_zstd_tar(local_download_path=None, output_filename=None):
    local_download_path = validate_local_download_path(local_download_path)
    if output_filename is None:
        output_filename = pathify(output_filename)
    logger.debug(f"Compressing files in {local_download_path} to {output_filename}")
    with tarfile.open(output_filename, "w|") as tar:
        tar.add(local_download_path, arcname=os.path.basename(local_download_path))

    logger.debug(f"Compressed the tar file using zstandard to {output_filename}")
    with open(output_filename, "rb") as tar_file:
        with open(f"{output_filename}.zst", "wb") as zst_file:
            cctx = zstd.ZstdCompressor(level=3)  # Compression level can be adjusted
            cctx.copy_stream(tar_file, zst_file)

    os.remove(output_filename)  # Remove the uncompressed tar file
    logger.debug(f"Compressed to {output_filename}.zst")
    return output_filename


def pathify(path):
    """Replaces a directory / with a valid filename"""
    if not path:
        return os.getcwd().replace("/", "_") + ".tar.zst"
    output = path.replace("/", "_") + ".tar.zst"
    return output[1:] if output.startswith("_") else output


def validate_local_download_path(local_download_path=None):
    if local_download_path is None:
        local_download_path = os.path.join(os.getcwd(), DEFAULT_LOCAL_DATA_PATH)
    if not os.path.exists(local_download_path):
        logger.debug(f"Creating directory {local_download_path}")
        os.makedirs(local_download_path)
    return local_download_path
