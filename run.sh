#!/bin/sh

modprobe w1-gpio && modprobe w1-therm
exec python -m app
