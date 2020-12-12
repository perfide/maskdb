FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

RUN \
  set -euxo pipefail && \
  ls -la /app/ && \
  find /app/ && \
  pip install --upgrade pip && \
  pip install -r requirements-docker.txt && \
  rm requirements-docker.txt

CMD ["gunicorn", "-b 0.0.0.0:5000", "maskdb:app"]

# [EOF]
