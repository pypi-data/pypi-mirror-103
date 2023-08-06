# Yokaranda-PythonLib (yokr)

# What is this?

Python3 client for Yokaranda SaaS.
Collects currently imported packages and user-submitted timeseries values,
batches the values in a cache in RAM and a cache in local SQLite file and
submits them to a Yokaranda server.

# How to install?

`pip install --extra-index-url https://test.pypi.org/simple/ yokr`

# How to add to requirements_to_freeze.txt ?

```
cat requirements_to_freeze.txt
--extra-index-url https://test.pypi.org/simple/
yokr
```

# What does requirements.txt look like?

```
pip freeze -r requirements_to_freeze.txt > requirements.txt
cat requirements.txt
--extra-index-url https://test.pypi.org/simple/
yokr==0.0.6
## The following requirements were added by pip freeze:
```

# How to use?

```python
import yokr

yokr.report_val('totally_not_centrifuge_rpm', 50000)
yokr.report_val('totally_not_centrifuge_rpm', 50000, report_time=1577814385.5)
```

# For package maintainers

## How to test?

```
$ cd yokr/
$ source venv/bin/activate
$ rm -rf build/ dist/ yokr.egg-info/
$ python3 setup.py sdist bdist_wheel
$ deactivate

$ cd test/
$ source venv/bin/activate
$ pip uninstall yokr
$ pip install yokr/dist/yokr-0.0.8-py3-none-any.whl
$ deactivate
```

## How to package

```
rm -rf build/ dist/ yokr.egg-info/
python3 setup.py sdist bdist_wheel
# unzip -lv dist/yokr-0.0.6-py3-none-any.whl | less
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## About original R version

### Basic R version usage for testing:

```
install.packages("uuid")
install.packages("openssl")
install.packages("lubridate")
install.packages("DBI")
install.packages("RSQLite")
install.packages("dplyr")


source(file='yokr.R')
hello()
libsInUse()
library(dplyr)

```

### Installing the package:

Install system dependencies:

```
sudo apt-get install libcurl4-openssl-dev
```

In R (Install dependencies):

```
install.packages("plyr")
install.packages("devtools")
install.packages("httr")
install.packages("jsonlite")
```

In shell:

```

```

Usage in R after installation:

```
library('yokaranda')
```
