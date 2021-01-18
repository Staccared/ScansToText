FROM ubuntu:20.04 as python-with-requirements

RUN apt-get -y update && \
  apt-get -y install \
    python3

# Install OS Deps:
#
# libgl1-mesa-glx, libglib2.0-0 required by python-cv2
# tzdata required by libglib2.0-0
# ghostscript required by us
# tesseract-* required by us
RUN \
  echo 'Etc/UTC' > /etc/timezone && \
  env DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
  apt-get install -y libgl1-mesa-glx libglib2.0-0 \
  ghostscript \
  tesseract-ocr tesseract-ocr-deu

# Actually only required at image build time, not at container run time
RUN apt-get install -y \
  python3-pip \
  python3-venv

ENV VIRTUAL_ENV=/opt/scanstotext/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# pip upgrade required for PyPDF2 building without errors
RUN python -m pip install --upgrade pip

# Install App Python dependencies
ADD requirements.txt /opt/scanstotext/requirements.txt
RUN pip install -r /opt/scanstotext/requirements.txt

# Install App
ADD scanstotext/ /opt/scanstotext/scanstotext
ADD very_simple_pipeline.py /opt/scanstotext/

WORKDIR /opt/scanstotext
ENTRYPOINT [ "python", "very_simple_pipeline.py" ]


