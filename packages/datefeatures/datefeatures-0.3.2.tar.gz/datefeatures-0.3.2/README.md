[![PyPI version](https://badge.fury.io/py/datefeatures.svg)](https://badge.fury.io/py/datefeatures)
[![datefeatures](https://snyk.io/advisor/python/datefeatures/badge.svg)](https://snyk.io/advisor/python/datefeatures)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/kmedian/datefeatures.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/kmedian/datefeatures/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/kmedian/datefeatures.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/kmedian/datefeatures/context:python)
[![deepcode](https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6ImttZWRpYW4iLCJyZXBvMSI6ImRhdGVmZWF0dXJlcyIsImluY2x1ZGVMaW50IjpmYWxzZSwiYXV0aG9ySWQiOjI5NDUyLCJpYXQiOjE2MTk1MzYxMzR9.N7NgWjiFb0RXjg2MK8jsmf_2KPL8cWtkUhz02uZ-k2w)](https://www.deepcode.ai/app/gh/kmedian/datefeatures/_/dashboard?utm_content=gh%2Fkmedian%2Fdatefeatures)


# datefeatures

## Table of Contents
* [Installation](#installation)
* [Usage](#usage)
* [Commands](#commands)
* [Support](#support)
* [Contributing](#contributing)


## Installation
The `datefeatures` [git repo](http://github.com/kmedian/datefeatures) is available as [PyPi package](https://pypi.org/project/datefeatures)

```
pip install datefeatures
```


## Usage
Check the [examples](examples) folder for notebooks.


## Commands
Install a virtual environment

```
python3 -m venv .venv  # see note below
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install jupyterlab
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `python -W ignore -m unittest discover`

Publish

```sh
pandoc README.md --from markdown --to rst -s -o README.rst
python setup.py sdist 
twine upload -r pypi dist/*
```

Clean up 

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```

## Support
Please [open an issue](https://github.com/kmedian/datefeatures/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/kmedian/datefeatures/compare/).
