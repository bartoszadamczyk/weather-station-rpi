# Weather station: RPi

Cloud based Raspberry Pi weather station

### Install dependencies:

```shell
pip install -r requirements.txt
```

### Save Dependencies

```shell
pip freeze > requirements.txt
```

### Run app

```shell
python -m app
```

### Run dev

```shell
black . && flake8 && mypy -m app
```
