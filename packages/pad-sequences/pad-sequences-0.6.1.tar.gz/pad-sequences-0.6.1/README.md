[![PyPI version](https://badge.fury.io/py/pad-sequences.svg)](https://badge.fury.io/py/pad-sequences)
[![pad-sequences](https://snyk.io/advisor/python/pad-sequences/badge.svg)](https://snyk.io/advisor/python/pad-sequences)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ulf1/pad-sequences.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf1/pad-sequences/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ulf1/pad-sequences.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ulf1/pad-sequences/context:python)
[![deepcode](https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6InVsZjEiLCJyZXBvMSI6InBhZC1zZXF1ZW5jZXMiLCJpbmNsdWRlTGludCI6ZmFsc2UsImF1dGhvcklkIjoyOTQ1MiwiaWF0IjoxNjE5NTQwMzIyfQ.iKciKcAPZiAqjT5iXJ2ad0ZX055zGkyB34VHW4QRG7o)](https://www.deepcode.ai/app/gh/ulf1/pad-sequences/_/dashboard?utm_content=gh%2Fulf1%2Fpad-sequences)

# pad-sequences
Pad variable length sequences with multiples features.

## Installation via pip
The `pad-sequences` [git repo](http://github.com/ulf1/pad-sequences) 
is available as [PyPi package](https://pypi.org/project/pad-sequences)

```sh
pip install "pad-sequences>=0.6.0"
```


## Usage

```py
from pad_sequences import pad_sequences_multi
import tensorflow as tf
# import torch

seq = []
seq.append([[1, 1, 1], [2, 2, 2]])
seq.append([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]])

n_samples = len(seq)
n_features = len(seq[0][0])
n_timesteps = 3

# for input sequences
padded = pad_sequences_multi(seq, padding='pre', value=0, 
                             truncating='pre', maxlen=n_timesteps)
# for output sequences
# padded = pad_sequences_multi(seq, padding='post', value=0, 
#                              truncating='post', maxlen=n_timesteps)

X = tf.reshape(padded, [n_samples, n_timesteps, n_features])
# X = torch.reshape(torch.tensor(padded), [n_samples, n_timesteps, n_features])
```


Check the [examples](http://github.com/ulf1/pad-sequences/examples) folder for notebooks.


## Appendix

### Install a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements-dev.txt
pip3 install -r requirements-demo.txt
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Other python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `pytest`

Publish

```sh
pandoc README.md --from markdown --to rst -s -o README.rst
python setup.py sdist 
twine upload -r pypi dist/*
```

### Clean up 

```sh
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### Debugging
* Notebooks to profile python code are in the [profile](http://github.com/ulf1/pad-sequences/profile) folder
