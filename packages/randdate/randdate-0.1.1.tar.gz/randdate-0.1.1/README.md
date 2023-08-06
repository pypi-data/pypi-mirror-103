[![PyPI version](https://badge.fury.io/py/randdate.svg)](https://badge.fury.io/py/randdate)
[![randdate](https://snyk.io/advisor/python/randdate/badge.svg)](https://snyk.io/advisor/python/randdate)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/kmedian/randdate.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/kmedian/randdate/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/kmedian/randdate.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/kmedian/randdate/context:python)
[![deepcode](https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6ImttZWRpYW4iLCJyZXBvMSI6InJhbmRkYXRlIiwiaW5jbHVkZUxpbnQiOmZhbHNlLCJhdXRob3JJZCI6Mjk0NTIsImlhdCI6MTYxOTU0MDM0N30.mqU-JDLOg9XOiZ0xoxHVsWFmm9sPiYnBGg49okrZzi8)](https://www.deepcode.ai/app/gh/kmedian/randdate/_/dashboard?utm_content=gh%2Fkmedian%2Franddate)

# randdate
Generate a list of random dates (datetime objects).


## Installation
The `randdate` [git repo](http://github.com/kmedian/randdate) is available as [PyPi package](https://pypi.org/project/randdate)

```
pip install randdate
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
Please [open an issue](https://github.com/kmedian/randdate/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/kmedian/randdate/compare/).
