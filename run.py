import click

from loguru import logger

from downloder import download


@click.group()
def cli():
    pass


@cli.command()
@click.argument("bucket_name", type=str)
@click.argument("folder_path", type=str)
@click.argument("local_download_path", type=str)
@click.argument("output_filename", type=str)
def perform(bucket_name, folder_path, local_download_path, output_filename):
    logger.info(f"Downloading files from {bucket_name}/{folder_path} to {local_download_path}")
    # Step 1: Download files from GCS
    download.download_files_from_gcs(bucket_name, folder_path, local_download_path)

    # Step 2: Compress the downloaded files into a .tar.zst file
    output = download.compress_files_to_zstd_tar(local_download_path, output_filename)
    logger.info(f"Compressed files to {output}")

    # Step 3: Cleanup
    # Optionally, you can delete the local files after compression to free up space
    # shutil.rmtree(local_download_path)


if __name__ == "__main__":
    cli()
