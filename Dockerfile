FROM python:3.7.4-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

ENV BUILD_DEPS="build-essential" \
    APP_DEPS="curl libpq-dev python-dev default-libmysqlclient-dev"

RUN apt-get update \
  && apt-get install -y ${BUILD_DEPS} ${APP_DEPS} --no-install-recommends \
  && pip install -r requirements.txt \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /usr/share/doc && rm -rf /usr/share/man \
  && apt-get purge -y --auto-remove ${BUILD_DEPS} \
  && apt-get clean

ARG FLASK_ENV="production"
ENV FLASK_ENV="${FLASK_ENV}" \
    PYTHONUNBUFFERED="true"

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
