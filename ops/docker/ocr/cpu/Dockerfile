FROM python:3.8 as runtime-image

ARG DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN mkdir -p /usr/share/man/man1/

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install --no-install-recommends --no-install-suggests -y \
    build-essential \
    curl \
    ca-certificates p11-kit \
    python3-dev \
    python3-distutils \
    python3-venv \
    openjdk-11-jre-headless \
    tesseract-ocr \
    libtesseract-dev \
    libpq-dev \
    python3-pip \
    libgl1-mesa-glx &&\
    apt clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U pip setuptools
RUN pip3 install calamari-ocr
COPY ops/docker/ocr/requirements.txt /
RUN --mount=type=cache,target=/root/.cache/pip3 pip3 install --no-cache-dir -r /requirements.txt

RUN mkdir -p /home/model-server/model-store
RUN mkdir /mozhi
RUN mkdir /services
COPY mozhi /mozhi
COPY api /api
COPY configs /configs
COPY data/SROIE2019/model-output /home/model-server/model-store
EXPOSE 8089

RUN chmod 777 api/start_calamari.sh
ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PYTHONPATH "${PYTHONPATH}:/api"
CMD api/start_calamari.sh