[![PyPI version](https://badge.fury.io/py/threesplit.svg)](https://badge.fury.io/py/threesplit)
[![threesplit](https://snyk.io/advisor/python/threesplit/badge.svg)](https://snyk.io/advisor/python/threesplit)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/kmedian/threesplit.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/kmedian/threesplit/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/kmedian/threesplit.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/kmedian/threesplit/context:python)
[![deepcode](https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6ImttZWRpYW4iLCJyZXBvMSI6InRocmVlc3BsaXQiLCJpbmNsdWRlTGludCI6ZmFsc2UsImF1dGhvcklkIjoyOTQ1MiwiaWF0IjoxNjE5NTQwNjI4fQ.YC9h-9S3cQqgPOlYq3WYA8SegkLEL4sFHN-DQAVQBY0)](https://www.deepcode.ai/app/gh/kmedian/threesplit/_/dashboard?utm_content=gh%2Fkmedian%2Fthreesplit)

# threesplit
Three-way data split into training set, validation set, and test set.


## Installation
The `threesplit` [git repo](http://github.com/kmedian/threesplit) is available as [PyPi package](https://pypi.org/project/threesplit)

```
pip install threesplit
```


## Usage
Check the [examples](examples) folder for notebooks.


## Commands
* Check syntax: `flake8 --ignore=F401`
* Remove `.pyc` files: `find . -type f -name "*.pyc" | xargs rm`
* Remove `__pycache__` folders: `find . -type d -name "__pycache__" | xargs rm -rf`

Publish

```sh
pandoc README.md --from markdown --to rst -s -o README.rst
python setup.py sdist 
twine upload -r pypi dist/*
```


## Support
Please [open an issue](https://github.com/kmedian/threesplit/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/kmedian/threesplit/compare/).
