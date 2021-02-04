FROM balenalib/raspberrypi3-debian-python:run

RUN apt-get update && apt-get upgrade \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libgpiod2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install w1thermsensor RPi.GPIO adafruit-circuitpython-dht

RUN mkdir -p /usr/src/app
COPY . /usr/src/app

WORKDIR /usr/src/app

RUN chmod +x run.sh
CMD [ "bash", "run.sh" ]
