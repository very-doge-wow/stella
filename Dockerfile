FROM python:3.11.1

USER root

WORKDIR app

COPY . .

RUN pip install pipenv && \
    pipenv install --system --deploy && \
    chmod +x stella.py && \
    ln -s /app/stella.py /usr/local/bin/stella

USER 1000

ENTRYPOINT ["stella"]
