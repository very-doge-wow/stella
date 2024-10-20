FROM python:3.13-alpine3.20@sha256:c38ead8bcf521573dad837d7ecfdebbc87792202e89953ba8b2b83a9c5a520b6 as helper

# renovate: datasource=pypi depName=pipenv versioning=pep440
ENV PIP_ENV_VERSION=2024.0.3

USER root

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN <<EOF
pip install pipenv==${PIP_ENV_VERSION} --no-cache-dir --upgrade
pipenv requirements --hash > requirements.txt
EOF

USER 1000

FROM python:3.13-alpine3.20@sha256:c38ead8bcf521573dad837d7ecfdebbc87792202e89953ba8b2b83a9c5a520b6

ARG IMAGE_VERSION=latest
ARG COMMIT_SHA=unknown

USER root

WORKDIR /app

COPY reader/ ./reader
COPY writer ./writer
COPY stella.py EXAMPLE/style.css ./
COPY --from=helper /app/requirements.txt .

RUN <<EOF
pip install --no-cache-dir --root-user-action ignore -r requirements.txt
chmod +x stella.py
ln -s /app/stella.py /usr/local/bin/stella
EOF

USER 1000

ENTRYPOINT ["stella"]

LABEL org.opencontainers.image.source="https://github.com/very-doge-wow/stella"
LABEL org.opencontainers.image.url="https://github.com/very-doge-wow/stella/pkgs/container/stella"
LABEL org.opencontainers.image.documentation="https://github.com/very-doge-wow/stella/blob/${COMMIT_SHA}/README.md"
LABEL org.opencontainers.image.version="${IMAGE_VERSION}"
LABEL org.opencontainers.image.revision="${COMMIT_SHA}"
LABEL org.opencontainers.image.vendor="very-doge-wow"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="stella"
LABEL org.opencontainers.image.description="stella is a free tool to help automatically generate helm chart documentation."
