FROM ubuntu:20.04 as python-with-requirements

RUN apt-get -y update && \
  apt-get -y install \
    python3

RUN apt-get install -y \
  python3-pip \
  python3-venv

ENV VIRTUAL_ENV=/opt/scanstotext/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD requirements.txt /opt/scanstotext/requirements.txt
RUN pip install -r /opt/scanstotext/requirements.txt

# libgl1-mesa-glx, libglib2.0-0 required by python-cv2
# tzdata required by libglib2.0-0
RUN \
  echo 'Etc/UTC' > /etc/timezone && \
  env DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
  apt-get install -y libgl1-mesa-glx libglib2.0-0


ADD src/ /opt/scanstotext/scanstotext

WORKDIR /opt/scanstotext/scanstotext
ENTRYPOINT [ "python" ]
CMD [ "Binarization.py" ]

