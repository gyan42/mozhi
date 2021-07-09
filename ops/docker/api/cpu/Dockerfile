#https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/backend.dockerfile
#export DOCKER_BUILDKIT=1

FROM python:3.8 as runtime-image

RUN pip3 install --upgrade cython
RUN pip3 install --no-cache-dir spacy

COPY ops/docker/api/cpu/requirements-heavy.txt /
RUN --mount=type=cache,target=/root/.cache/pip3 pip3 install --no-cache-dir -r /requirements-heavy.txt

ARG DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN mkdir -p /usr/share/man/man1/

RUN apt-get update && \
    apt-get install --no-install-recommends --no-install-suggests -y \
    gcc \
    curl \
    ca-certificates p11-kit \
    openjdk-11-jdk \
    tesseract-ocr \
    libtesseract-dev \
    libpq-dev \
    libgl1-mesa-glx &&\
    apt clean && rm -rf /var/lib/apt/lists/*

COPY ops/docker/api/requirements-light.txt /
RUN --mount=type=cache,target=/root/.cache/pip3 pip3 install --no-cache-dir -r /requirements-light.txt

RUN python -m spacy download en_core_web_sm

RUN mkdir /mozhi
RUN mkdir /services
COPY mozhi /mozhi
COPY api /api
RUN mkdir -p /home/model-server/model-store
EXPOSE 8088 8080 8081 8082 6543 6544 6545 7070 7071

RUN chmod 777 api/start.sh
ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PYTHONPATH "${PYTHONPATH}:/api"
CMD api/start.sh