# ScansToText

Extracting high quality text from scanned images


## Docker

Build Docker image:

```
docker build . -t scanstotext:latest
```

Run `Binarization.py` with local test file:

```
docker run -it --rm \
  -v "$(pwd):/data" \
  -u $(id -u) \
  scanstotext Binarization.py \
  /data/test/testdata/Test1.tif /data/test/testdata/out.jpg
```
