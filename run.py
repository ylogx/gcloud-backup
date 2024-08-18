import click

from loguru import logger

from downloder import download


@click.group()
def cli():
    pass


@cli.command()
@click.option("-b", "--bucket-name", type=str, required=True, help="Name of the GCS bucket")
@click.option("-f", "--folder-path", type=str, required=True, help="Path to the folder in the bucket")
@click.option("-l", "--local-download-path", type=str, required=False, help="Local path to download the files")
@click.option("-o", "--output-filename", type=str, required=False, help="Name of the output file")
def perform(bucket_name, folder_path, local_download_path, output_filename):
    logger.info(f"Downloading files from {bucket_name}/{folder_path} to {local_download_path}")
    downloader = download.GoogleCloudStorageDownloader(
        bucket_name,
        folder_path,
        local_download_path,
    )
    # Step 1: Download files from GCS
    downloader.download_files(bucket_name, folder_path, local_download_path)

    # Step 2: Compress the downloaded files into a .tar.zst file
    output = downloader.compress_files(local_download_path, output_filename)
    logger.info(f"Compressed files to {output}")

    # Step 3: Cleanup
    # Optionally, you can delete the local files after compression to free up space
    # shutil.rmtree(local_download_path)


if __name__ == "__main__":
    cli()
