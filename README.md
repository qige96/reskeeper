# Reskeeper
A lightweight management system for applying and releasing exclusive resources.

## Quickstart

```python
from reskeeper import ResourceKeeper

resources = [
    "resource1", 
    "resource2",
]

rk = ResourceKeeper() # new resource keeper
rk.load(resources)    # load a batch of data

res1 = rk.get()       # get a resource
res2 = rk.get()       # get one more resource
res3 = rk.get()       # None, no resource available

print(res1)
print(res2.res_id, res2.data)
print(res3)

rk.release(res1)     # release a resource

res4 = rk.get()      # one resource available

print(res4.to_dict())

```