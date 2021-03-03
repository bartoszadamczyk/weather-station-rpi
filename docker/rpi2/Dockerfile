FROM balenalib/raspberrypi3-debian-python:run

RUN apt-get update && apt-get upgrade \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libgpiod2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install w1thermsensor RPi.GPIO adafruit-circuitpython-dht boto3

RUN mkdir -p /usr/src
COPY app /usr/src/
COPY run.sh /usr/src/

WORKDIR /usr/src

RUN chmod +x run.sh
CMD [ "bash", "run.sh" ]
