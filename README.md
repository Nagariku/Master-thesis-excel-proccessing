# Master thesis data processing
## in progress

[![Python package](https://github.com/grigsos/Master-thesis-excel-proccessing/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/grigsos/Master-thesis-excel-proccessing/actions/workflows/main.yml)

Group:
Grigorii Osipov
Jacques Tatossian

## Installation

Ensure you have python 3.10+ installed and VSCode with Python extension installed.

In VSCode in Terminal
```console
$ git clone https://github.com/Nagariku/Master-thesis-excel-proccessing.git
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py
$ pip install -r requirements.txt
```

## Running program
Place your Excel files in the folder under the name that is listed in config.ini under "inputFolder". By default it is "Excel_surveys"
If needed, adjust the settings in config.ini to your needs.

```console
$ python run.py 
```

## Running tests
These tests are written using pytest. To run them, use the following command:

```console
$ python -m pytest
```
The tests are located in the tests folder and will test the functionality of the program and config file.

## Documentation


## Settings
 to be added
-How to use
-Settings in config file
-Troubleshooting
