import os
import aiofiles
import asyncio
from google.cloud import storage
from loguru import logger


class GoogleCloudStorageDownloader(object):
    def __init__(self, bucket_name, folder_path, local_download_path=None):
        self.bucket_name = bucket_name
        self.folder_path = folder_path
        self.local_download_path = local_download_path
        self._validate_local_download_path()

    def download_and_compress(self, output_filename=None, gcloud_project=None) -> str:
        """Downloads files from a Google Cloud Storage bucket to a local directory and compresses them"""
        asyncio.run(self.download_files(gcloud_project=gcloud_project))
        return self.compress_files(output_filename=output_filename)

    async def download_files(self, gcloud_project=None):
        """Downloads files from a Google Cloud Storage bucket to a local directory"""
        logger.info(f"Downloading files from {self.bucket_name}/{self.folder_path} to {self.local_download_path}")
        storage_client = storage.Client(project=gcloud_project)
        bucket = storage_client.bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=self.folder_path)

        tasks = []
        for blob in blobs:
            if not blob.name.endswith("/"):  # ignore directories
                destination_path = os.path.join(self.local_download_path, os.path.relpath(blob.name, self.folder_path))
                if os.path.exists(destination_path):
                    logger.info(f"File {destination_path} already exists, skipping download.")
                    continue

                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                temp_path = destination_path + ".tmp"
                tasks.append(self.download_blob(blob, temp_path, destination_path))

        await asyncio.gather(*tasks)

    async def download_blob(self, blob, temp_path, destination_path):
        try:
            logger.debug(f"Downloading {blob.name} to {temp_path}")
            await asyncio.to_thread(self._sync_download_blob, blob, temp_path)
            os.rename(temp_path, destination_path)
            self._set_file_times(blob, destination_path)
            logger.debug(f"Downloaded {blob.name} to {destination_path}")
        except Exception as e:
            logger.error(f"Failed to download {blob.name}: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _sync_download_blob(self, blob, temp_path):
        with open(temp_path, "wb") as temp_file:
            blob.download_to_file(temp_file)

    def _set_file_times(self, blob, file_path):
        """Set the access and modification times of the file based on the blob properties"""
        created_time = blob.time_created.timestamp()
        updated_time = blob.updated.timestamp()
        os.utime(file_path, (created_time, updated_time))

    def compress_files(self, output_filename=None):
        """Compresses the downloaded files into a tar.zst file"""
        import tarfile
        import zstandard as zstd

        if output_filename is None:
            output_filename = _pathify(self.folder_path)
        logger.info(f"Compressing files in {self.local_download_path} to {output_filename}")
        with tarfile.open(output_filename, "w|") as tar:
            tar.add(self.local_download_path, arcname=os.path.basename(self.local_download_path))

        compressed_filename = output_filename + ".zst"
        logger.debug(f"Compressed the tar file using zstandard to {compressed_filename}")
        with open(output_filename, "rb") as tar_file:
            with open(compressed_filename, "wb") as zst_file:
                cctx = zstd.ZstdCompressor(level=3)  # Compression level can be adjusted
                cctx.copy_stream(tar_file, zst_file)

        os.remove(output_filename)  # Remove the uncompressed tar file
        logger.debug(f"Compressed to {compressed_filename}")
        return compressed_filename

    def _validate_local_download_path(self):
        if self.local_download_path is None:
            self.local_download_path = os.path.join(os.getcwd(), os.path.basename(self.folder_path))
        if not os.path.exists(self.local_download_path):
            logger.debug(f"Creating directory {self.local_download_path}")
            os.makedirs(self.local_download_path)


def _pathify(path):
    """Replaces a directory / with a valid filename"""
    assert path is not None and path != "", "Path cannot be empty"
    output = os.path.basename(path).replace("/", "_").rstrip("_") + ".tar"
    return output[1:] if output.startswith("_") else output
