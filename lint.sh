#!/bin/sh

black . && flake8 && mypy .
