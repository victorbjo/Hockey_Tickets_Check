FROM ubuntu:22.04

# Running locally on my machine requires adding `--allow-insecure-repositories` to
# the update. For some reason Docker do not want to validate its certificate.

RUN apt-get update \
    && apt-get install software-properties-common -y \
    && apt-get install -y \
    python3-pip=22.0.2+dfsg-1 \
  && rm -rf /var/lib/apt/lists/* \
  && ln -s /usr/bin/python3 /usr/bin/python

  
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

#COPY migrations/*.sql migrations/
COPY src /app

ENV EMAIL=''
ENV PASSWORD=''
ENV RECEIVERS=''
ENV SMTP_SERVER=''

CMD ["python", "/app/script.py"]