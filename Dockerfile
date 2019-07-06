FROM python:latest
LABEL maintainer="shinichir0 <github@shinichironaito.com>"

ARG chrome_driver_version="76.0.3809.25"

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV HOME /root

COPY Pipfile ./
COPY Pipfile.lock ./

RUN apt-get update && apt-get upgrade -y && \
  apt-get install -y --no-install-recommends apt-utils curl ca-certificates cron git libfontconfig fontconfig unzip && \
  mkdir -p /usr/share/fonts/opentype/noto && \
  curl -O https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip && \
  unzip NotoSansCJKjp-hinted.zip -d /usr/share/fonts/opentype/noto && \
  rm NotoSansCJKjp-hinted.zip && \
  fc-cache -f && \
  apt-get install -y --no-install-recommends fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatspi2.0-0 libgtk-3-0 libnspr4 libnss3 libx11-xcb1 libxtst6 lsb-release xdg-utils && \
  curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
  dpkg -i google-chrome-stable_current_amd64.deb && \
  rm google-chrome-stable_current_amd64.deb && \
  curl -O https://chromedriver.storage.googleapis.com/${chrome_driver_version}/chromedriver_linux64.zip && \
  unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
  rm chromedriver_linux64.zip && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get purge -y unzip && \
  apt-get autoremove -y && apt-get autoclean -y && \
  pip install --upgrade pip setuptools pipenv && \
  set -ex && pipenv install --deploy --system && \
  rm -rf ${HOME}/.cache/pip

RUN echo 'HOME=/root' >> /etc/crontab && \
  echo 'PYTHONPATH=/root/app:${PYTHONPATH}' >> /etc/crontab && \
  echo '*/15 * * * * root python /root/app/main.py' >> /etc/crontab
