FROM apache/airflow:2.1.3
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
        chromium \
        vim \
        wget \
        libglib2.0-0 \
        libnss3 \
        libgconf-2-4 \
        libfontconfig1 \
  && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt install -y ./google-chrome-stable_current_amd64.deb \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* 

USER airflow

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt