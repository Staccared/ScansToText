# ScansToText

Extracting high quality text from scanned images


## Docker

Build Docker image:

```
docker build . -t scanstotext:latest
```

Run `very_simple_pipeline.py` with local test file:

```
docker run --rm -v "$(pwd):/data" -u $(id -u) \
  scanstotext \
  /data/test/testdata/Test-Grüne001.pdf
```
