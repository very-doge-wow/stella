FROM python:3.12-alpine3.19

USER root

WORKDIR app

COPY reader ./reader/
COPY writer ./writer/
COPY stella.py Pipfile Pipfile.lock EXAMPLE/style.css ./

RUN <<EOF
pip install pipenv
pipenv install --system --deploy
chmod +x stella.py
ln -s /app/stella.py /usr/local/bin/stella
EOF

USER 1000

ENTRYPOINT ["stella"]
