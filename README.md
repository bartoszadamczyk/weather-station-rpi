# Weather station: Raspberry Pi

[![Deploy Prod](https://github.com/bartoszadamczyk/weather-station-rpi/actions/workflows/deploy_prod.yml/badge.svg?branch=main)](https://github.com/bartoszadamczyk/weather-station-rpi/actions/workflows/deploy_prod.yml)
[![License: MIT](https://img.shields.io/github/license/bartoszadamczyk/weather-station-rpi)](https://github.com/bartoszadamczyk/weather-station-rpi/blob/main/LICENSE)

Cloud based Raspberry Pi weather station

### Repositories

- [Cloud App](https://github.com/bartoszadamczyk/weather-station-cloud)
    - [React App](https://github.com/bartoszadamczyk/weather-station-cloud/app) Frontend React app that displays live
      readings. Stack: `Netlify`, `TypeScript`, `React`, `Immer`, `WebSockets`, `i18next`, `antd`, `Sentry`, `Jest`,
      `ESLint`, `GitHub Actions`
    - [Serverless API](https://github.com/bartoszadamczyk/weather-station-cloud/serverless) Serverless API bundled with
      Serverless and hosted on AWS Lambda. Stack: `Serverless`, `TypeScript`, `DynamoDB`, `SQS`, 
      `AWS API Gateway (with WebSockets)`, `AJV`, `Sentry`, `Mocha`, `Chai`, `Sinon`, `ESLint`, `GitHub Actions`
    - [Terraform](https://github.com/bartoszadamczyk/weather-station-cloud/terraform) Stack: `Terraform`, `TFLint`, 
      `GitHub Actions`
- [Raspberry Pi](https://github.com/bartoszadamczyk/weather-station-rpi) Raspberry Pi worker deployed with balena.io.
  Stack `Raspberry Pi`, `Linux`, `balena.io`, `Docker`, `Python`, `AsyncIO`, `SQS`, `Mypy`, `Black`, `Flake8`, `Sentry`
  and `GitHub Actions`

![All sensors module](docs/all-sensors-module.jpg)

## Sensors and relays

### DS18B20: Temperature Sensor

Fast, accurate, and cheap temperature sensor. You can't go wrong with that one. It is available standalone as well as a
pre-wired waterproof version.

- Depending on the housing and cable used it can measure a temperature from -55°C to +125° with a decent accuracy of
  ±0.5°C.
- Each sensor has a unique device ID.
- It can work with both 3.3v and 5v.
- Sensor is using 1-Wire protocol that can support multiple sensors connected to one GPIO.
- `GPIO 4` is used by default, you can connect all your sensors to one GPIO.
- Especially for longer cables pull up resistor of 4.7k-10k ohm is required.

You can get it on [The PiHut](https://thepihut.com/products/waterproof-ds18b20-digital-temperature-sensor-extras)
, [Adafruit](https://www.adafruit.com/product/381) or Amazon.

![Weather station schematics for DS18B20 sensor](docs/weather-station-schematics-DS18B20.svg)

### DHT22: Temperature and Humidity Sensor

A basic sensor that is quite slow and buggy. On paper, you can get a reading every two seconds however protocol that is
used by this sensor is quite often crashing, hence in practice, you can the readings only a few times per minute.
Because of the errors in the protocol, the reading is sometimes incorrect. If you need just a temperature sensor, go for
DS18B20. If you got some extra budget go for the BME280 or BME680.

- Temperature readings in the range of -40 to 80°C with ±0.5°C accuracy.
- Humidity readings in the range of 0-100% with ±2-5% accuracy.
- It can work with both 3.3v and 5v.
- It requires one GPIO per one sensor together with the pull-up resistor.
- This project suggests using `GPIO 17`, `GPIO 27`, `GPIO 22`, `GPIO 23` and `GPIO 24`.
- No unique id, GPIO number is used as an ID.
- Pull up resistor of 4.7k-10k ohm is required.

You can get it on [The PiHut](https://thepihut.com/products/dht22-temperature-humidity-sensor-extras)
, [Adafruit](https://www.adafruit.com/product/385), or Amazon.

![Weather station schematics for DHT22 sensor](docs/weather-station-schematics-DHT22.svg)

### BME680: Temperature, Humidity, Pressure, Altitude and Gas Sensor

Overall very nice sensor, accurate, stable and versatile. On board chip is from Bosch, supports temperature, humidity,
pressure, altitude and gas, although the last two require calibration.

You can get it
on [The PiHut](https://thepihut.com/products/adafruit-bme680-temperature-humidity-pressure-and-gas-sensor-ada3660)
and [Pimoroni](https://shop.pimoroni.com/products/bme680-breakout)

![Weather station schematics for BME680 sensor](docs/weather-station-schematics-BME680.svg)

### Relays

You can use GPIOs as an output for your alarms. This can be used to control relays or other devices. **Remember to
protect your GPIOs! Don't connect relays directly to your Raspberry Pi. This is going to break your board!** You need
some transistors, diodes, resistors and preferably an optocoupler to protect your device. If you don't want to build it
yourself, buy a ready-made relay board. Just remember to pick one compatible with Raspberry Pi 3v3 GPIOs, like the one
from [WaveShare](https://www.waveshare.com/wiki/RPi_Relay_Board).

- WaveShare Relay board is using `GPIO 26`, `GPIO 20`, `GPIO 21`.
- You can also use `GPIO 19`, `GPIO 16`, `GPIO 13`, `GPIO 6`, `GPIO 12` and `GPIO 5`.

You can get it on [The PiHut](https://thepihut.com/products/raspberry-pi-relay-board) or Amazon.

![Weather station schematics for relay](docs/weather-station-schematics-relay.svg)

## How to deploy?

1. If you want to use the dashboard, follow the steps
   in [Cloud API](https://github.com/bartoszadamczyk/weather-station-cloud). You need `AWS_ACCESS_KEY_ID`
   , `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` and `AWS_SQS_DATA` from there.
2. Create a free [balena.io](balena.io) account (10 devices are for free!).
3. Create your first `balena application`. Flash your device, connect to the internet and turn it on.
4. Fork and clone this repository. You can deploy code to balena with:
    - [Github actions](./.github/workflows)
        - Edit deploy workflows to match your setup:
            - Use correct docker file for your device (for rpi2 you can use rpi3)
            - In your `Repository` -> `Settings` -> `Actions secrets` add:
                - `BALENA_API_TOKEN`
                - `BALENA_APPLICATION_NAME_RPI_2` or any other vars you want to use
    - Or manually with [git push](https://www.balena.io/docs/learn/deploy/deployment/#git-push)
        - Copy correct `Dockerfile` from [docker/](docker) directory into your `root dir`
        - Git push to balena
5. In balenaCloud, in `Device Configuration` set `Define DT overlays` to `"w1-gpio"`.
5. Great! Your Weather Station should work and already detect DS18B20 Temperature sensors!
6. Now, have a look at the Device Configuration below to enable more features.

## Device Configuration

You can configure more features with `Device service variables`:

| Feature                       | `ENV VARIABLES`                                                                       | Format       |
|-------------------------------|---------------------------------------------------------------------------------------|--------------|
| Override `BALENA_DEVICE_UUID` | `DEVICE_ID`                                                                           | `string`     |
| Enable Sentry                 | `SENTRY_DSN`, `SENTRY_ENVIRONMENT`                                                    | `string`     |
| Enable DHT22 sensors          | `DHT22_PINS`                                                                          | `[17]`       |
| Enable BME680 sensor          | `ENABLE_BME680`                                                                       | `True`       |
| Enable Relays                 | `RELAY_PINS`                                                                          | `[26,20,21]` |
| Enable LiveSQSConsumer        | `AWS_ACCESS_KEY_ID` ,`AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` and `AWS_SQS_DATA` | `string`     |

## Supported Devices

- Raspberry Pi 2 (armv7hf and up)
- Raspberry Pi 3
- Raspberry Pi 4

## Development

### Install dependencies:

```shell
pip install -r requirements.txt
```

### Save Dependencies

```shell
pip freeze > requirements.txt
```

### Run lint

```shell
./lint.sh
```

### Run test

```shell
./test.sh
```

## Sources

- https://pinout.xyz/
- https://www.circuito.io/app
- https://lastminuteengineers.com/electronics/basic-electronics/

## Backlog
[Available in weather-station-cloud repo](https://github.com/bartoszadamczyk/weather-station-cloud#backlog)
