# weather-station-rpi

Cloud based Raspberry Pi weather station

## Local installation

### Install Python

- [Source](https://swapps.com/blog/how-to-configure-virtualenvwrapper-with-python3-in-osx-mojave/)

Run:

```shell
brew install python
```

To your `.zshrc` add:

```shell
export PATH="/usr/local/opt/python/libexec/bin:/usr/local/sbin:$PATH"
```

Run:

```shell
pip install virtualenv
pip install virtualenvwrapper
```

To your `.zshrc` add:

```shell
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/codeplace
source /usr/local/bin/virtualenvwrapper.sh
```

Source your .zshrc or refresh terminal. Now you can `mkvirtualenv weather`, `lsvirtualenv`, `workon weather`,
`deactivate` and `rmvirtualenv weather`!

### Install dependencies:

```shell
pip install -r requirements.txt
```
