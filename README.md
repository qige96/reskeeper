# Reskeeper
[![version](https://img.shields.io/static/v1.svg?label=version&message=0.1.1&color=blue)](https://github.com/qige96/reskeeper)
[![docs](https://img.shields.io/static/v1.svg?label=docs&message=rtds&color=green)](https://reskeeper.readthedocs.io/en/latest/)

A lightweight management system for applying and releasing exclusive resources.


## Introduction

Considering these scenarios: you are doing web crapping that 
requiring proxies with multi-threads, and each thread can only 
use one proxy and one proxy can only be used by one thread at 
one time; or you are doing monkey tests for login process of 
your several applications at one time, each application can 
only use one test account and each account can only be used 
by one application at one time. You will need to manage the 
applying and releasing of these **exclusive resources**, and 
here is this little system taht can help.

## Installation
You can install it by just one command
```shell
pip install reskeeper
```
or
```shell
git install git+https://github.com/qige96/reskeeper.git
```

## Quick Start

```python
from reskeeper import ResourceKeeper

resources = [
    "resource1", 
    "resource2",
]

rk = ResourceKeeper()     # create a resource keeper instance
rk.load(resources)        # load a batch of data

res1 = rk.get()           # get a resource
res2 = rk.get()           # get one more resource
res3 = rk.get()           # None, no resource available

print(res1)               # <res_id: 1>
print(res2.res_id, 
        res2.data)        # (2, "resource2")
print(res3)               # None    

rk.release(res1)          # release a resource

res4 = rk.get()           # one resource available

print(res4.to_dict())     # {'res_id': 1, 'data': 'resource1'}

```

## Documentation

see https://reskeeper.readthedocs.io