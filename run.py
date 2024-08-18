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
@click.option("-p", "--gcloud-project", type=str, required=False, help="Name of the GCP project")
def perform(bucket_name, folder_path, local_download_path, output_filename, gcloud_project):
    downloader = download.GoogleCloudStorageDownloader(
        bucket_name,
        folder_path,
        local_download_path,
    )
    downloader.download_files(gcloud_project=gcloud_project)
    output = downloader.compress_files(output_filename=output_filename)
    logger.info(f"Compressed files to {output}")


if __name__ == "__main__":
    cli()
