# Reskeeper
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


## User Guide
To begin, just import the module and new an instance:
```python
from reskeeper import ResourceKeeper
rk = ResourceKeeper()
```
Then you have a resource keeper that provides key functionalites
for managing resources.

Once you have a resource keeper, you can load into a batch of data.
Let's take the test account management as an example.
```python
resources = [
    {'username':'user1', 'password':123},
    {'username':'user2', 'password':456},
]
rk.load(resources)
```
The `load` method will take an iterable as augument and sequentially
add resources into the resources pool and availble set.
`ResourceKeeper` will mark each added resource with a resource id. 
Now there are two resources in the pool and both are available.
```python
print(rk.size)               # 2
print(rk.avail_num)          # 2
```

When requiring an account, just call the method `get`, and a 
resource will be returned, or None if no resource available.
```python
res1 = rk.get()
res2 = rk.get()

print(rk.size)               # 2
print(rk.avail_num)          # 0

res3 = rk.get()              # None
```
The `get` method returns a `Resource` object, a wrapper for the 
resource id and resource data.
```python
print(res1.res_id, res.data) # 1, {'username':'user1', 'password':123}
print(res3)                  # None
```

After using the resource, it should be released so that it can be used 
by others. To release a resource, call the method `release`
```python
rk.release(res1)
print(res1.to_dict()) # {'res_id': None, 'data': None}
```
The `release` method will add the given resource into available set 
again, and the user lose the resource now.


One resource can be added or removed from `ResourceKeeper`
```python
rk.add({'username': 'user3', 'password': 789})
print(rk.size, rk.avail_num) # 3, 2

rk.remove(res2)
print(rk.size, rk.avail_num) # 2, 1
```

`ResourceKeeper` also provides two helpers for loading data from 
csv and json files.
```csv
user1,123
user2,456 
```
To load the csv file above, 
```python
rk2 = ResourceKeeper()
rk2.load_from_csv("./accounts.csv")
```

```json
[
    {"username": "user1", "password": 123},
    {"username": "user2", "password": 456},
]
```
To load the json file above,
```python
rk3 = ResourceKeeper()
rk3.load_from_json("./accounts_array.json")
```

Note that inside a json file must be an array, not an object. 
if the json file is like this:
```json
{
    "accounts": [
        {"username": "user1", "password": 123},
        {"username": "user2", "password": 456},
    ]
}
```
Then the `load_from_json` method will only load one data into 
the resources pool: it regnoise the object key "accounts" as 
a resource.
```python
rk4 = ResourceKeeper()
rk4.load_from_json("./accounts_object.json")
res = rk4.get()
print(res.to_dict())        # {'res_id': 1, 'data': 'accounts'}
```

## Customization
The `ResourceKeeper` consist of two parts: a map that stores all 
resources, and a set that maintains all available resources(id). 
Both the two key components can be customized by users. 

When a resource was added, an id was generated and the map storage 
maps the resource id to that resource data. By default, `ResourceKeeper` 
uses a python dict wrapper as the storage map. Users can make 
their own maps that meet their own needs, as long as their maps 
implementing three interfaces: `get`, `put`, and `delete`. The 
three interfaces hehave the same like `get`, `__setitem__`, and 
`__del__` of python dict. Users are suggested to examine and extend 
the base class `reskeeper.poolmaps.PoolMapABC`. 
An example is the encapsulation of sqlite3 to be a map. It can 
be found in [`reskeeper.poolmaps.SimpleSqliteMap`](http://www.baidu.com).

The other component is a set that maintains all ids of available 
resources. When users call `rk.get()` to apply for a resource, 
the `avail_set` pop out a `res_id`, then the keeper return a copy 
of resource related to that id. When `rk.release(res)` is invoked, 
the keeper destroy the resource(actually the copy), and add the 
`res_id` bake into `avail_set`. Thus, an available set should 
implements four interaces: `contains`, `add`, `pop` and `delete`. 
Likewise, users are suggested to examine and extend the base class 
`reskeeper.availsets.AvailSetABC`. The default available set 
adopted by `ResourceKeeper` is `reskeeper.availsets.LinkedQueue` 
which is a linked list that has some queue and set features 
(not have same element, but in a queue order).