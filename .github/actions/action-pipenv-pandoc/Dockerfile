ARG PYTHON_IMAGE_VERSION=3
FROM python:$PYTHON_IMAGE_VERSION

RUN pip install --upgrade pip \
 && pip install pipenv \
 && python --version ; pip --version ; pipenv --version

RUN apt-get update && \
    apt-get install -y pandoc

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
