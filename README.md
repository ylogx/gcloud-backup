Google Cloud Storage Backup
===========================

Have you gone through the pain of downloading files one-by-one from a Google Cloud Storage bucket?

Easily backup your Google Cloud Storage (GCS) bucket directories to your local machine or NAS with this CLI tool.
Leveraging Async IO for concurrent downloads, it ensures a fast and efficient download process.
The tool is fault-tolerant, allowing you to resume downloads after network interruptions.
It also compresses your files into a single tar file and uses zstd for optimal storage efficiency & speed.
Try it now to speed up your GCS backup process!

Installation
------------

To install the dependencies, run the following command:

```bash
make init # Install dependencies and setup poetry virtual environment
```

Getting Started
---------------

### Usage
To see the available options, run the following command:
```bash
poetry run python run.py --help

Usage: run.py cp [OPTIONS]

Options:
  -b, --bucket-name TEXT          Name of the GCS bucket  [required]
  -f, --folder-path TEXT          Path to the folder in the bucket  [required]
  -l, --local-download-path TEXT  Local path to download the files
  -o, --output-filename TEXT      Name of the output file
  -p, --gcloud-project TEXT       Name of the GCP project
  --help
```

### Downloading files from GCS
To download files from a GCS bucket, run the following command:

```bash
poetry run python run.py cp \
    --bucket us.artifacts.foobar.appspot.com \
    --folder-path containers/images \
    --gcloud-project foobar
# poetry run cp -b us.artifacts.foobar.appspot.com -f containers/images -p foobar # Shorthand format

2024-08-18 01:55:46.300 | DEBUG    | downloder.download:_validate_local_download_path:89 - Creating directory /Users/example/gcloud-downloader/images
2024-08-18 01:55:46.300 | INFO     | downloder.download:download_files:22 - Downloading files from us.artifacts.lineage-sc.appspot.com/containers/images to /Users/example/gcloud-downloader/images
2024-08-18 01:55:46.729 | DEBUG    | downloder.download:download_blob:43 - Downloading containers/images/file1
aa9e90e8b to /Users/example/gcloud-downloader/images/file1.tmp
2024-08-18 01:55:46.730 | DEBUG    | downloder.download:download_blob:43 - Downloading containers/images/file2
aeb790a03 to /Users/example/gcloud-downloader/images/file2.tmp
2024-08-18 01:55:46.731 | DEBUG    | downloder.download:download_blob:43 - Downloading containers/images/file3
67d570afa to /Users/example/gcloud-downloader/images/file3.tmp
...
2024-08-18 01:59:01.111 | DEBUG    | downloder.download:download_blob:47 - Downloaded containers/images/file1 to /Users/example/gcloud-downloader/images/file1
2024-08-18 01:59:01.462 | DEBUG    | downloder.download:download_blob:47 - Downloaded containers/images/file2 to /Users/example/gcloud-downloader/images/file2
2024-08-18 01:59:07.763 | DEBUG    | downloder.download:download_blob:47 - Downloaded containers/images/file3 to /Users/example/gcloud-downloader/images/file3
2024-08-18 01:59:07.768 | INFO     | downloder.download:compress_files:70 - Compressing files in /Users/example/gcloud-downloader/images to images.tar
2024-08-18 01:59:28.653 | DEBUG    | downloder.download:compress_files:75 - Compressed the tar file using zstandard to images.tar.zst
2024-08-18 01:59:49.002 | DEBUG    | downloder.download:compress_files:82 - Compressed to images.tar.zst
2024-08-18 01:59:49.003 | INFO     | __main__:cp:26 - Compressed files to images.tar.zst
```

You can find your downloaded files in the `images.tar.zst` file in the current directory as shown by logs above.
You can also specify the local download path using the `--local-download-path` option and the output filename using the `--output-filename` option.
