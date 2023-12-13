FROM python:3.12.1-slim

USER root

WORKDIR app

COPY reader ./reader/
COPY writer ./writer/
COPY stella.py Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system --deploy && \
    chmod +x stella.py && \
    ln -s /app/stella.py /usr/local/bin/stella

USER 1000

ENTRYPOINT ["stella"]
