Google Cloud Storage Downloader
===============================

Installation
------------
To install the dependencies, run the following command:

```bash
make init # Install dependencies and setup poetry virtual environment
```

Run
---

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
# poetry run cp -b us.artifacts.foobar.appspot.com -f containers/images -p foobar
```
