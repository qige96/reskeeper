.. reskeeper documentation master file, created by
   sphinx-quickstart on Fri Apr  5 22:11:06 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Reskeeper
=====================================

A lightweight management system for applying and releasing exclusive resources.

.. toctree
   :maxdepth: 2
   :caption: Contents:


Installation
----------------
You can install it by just one command
::

   pip install reskeeper

or::

   git install git+https://github.com/qige96/reskeeper.git


Quick Start
---------------------
Here is a mini example
::

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




User Guide
--------------
To begin, just import the module and new an instance
::

    from reskeeper import ResourceKeeper
    rk = ResourceKeeper()

Then you have a resource keeper that provides key functionalites
for managing resources.

Once you have a resource keeper, you can load into a batch of data.
Let's take the test account management as an example::

    resources = [
        {'username':'user1', 'password':123},
        {'username':'user2', 'password':456},
    ]
    rk.load(resources)

The ``load`` method will take an iterable as augument and sequentially
add resources into the resources pool and availble set.
`ResourceKeeper` will mark each added resource with a resource id. 
Now there are two resources in the pool and both are available::

    print(rk.size)               # 2
    print(rk.avail_num)          # 2


When requiring an account, just call the method `get`, and a 
resource will be returned, or None if no resource available::

    res1 = rk.get()
    res2 = rk.get()

    print(rk.size)               # 2
    print(rk.avail_num)          # 0

    res3 = rk.get()              # None

The ``get`` method returns a ``Resource`` object, a wrapper for the 
resource id and resource data
::

    print(res1.res_id, res1.data) # 1, {'username':'user1', 'password':123}
    print(res3)                  # None


After using the resource, it should be released so that it can be used 
by others. To release a resource, call the method ``release`` 
::

    rk.release(res1)
    print(res1.to_dict()) # {'res_id': None, 'data': None}

The ``release`` method will add the given resource into available set 
again, and the user lose the resource now.


One resource can be added or removed from `ResourceKeeper` 
::

    rk.add({'username': 'user3', 'password': 789})
    print(rk.size, rk.avail_num) # 3, 2

    rk.remove(res2)
    print(rk.size, rk.avail_num) # 2, 1


``ResourceKeeper`` also provides two helpers for loading data from 
csv and json files
::

    user1,123
    user2,456 

To load the above csv file above
::

    rk2 = ResourceKeeper()
    rk2.load_from_csv("./accounts.csv")


or json file
::

    [
        {"username": "user1", "password": 123},
        {"username": "user2", "password": 456},
    ]

To load the json file above
::

    rk3 = ResourceKeeper()
    rk3.load_from_json("./accounts_array.json")


Note that inside a json file must be an array, not an object. 
if the json file is like this
::

    {
        "accounts": [
            {"username": "user1", "password": 123},
            {"username": "user2", "password": 456},
        ]
    }

Then the ``load_from_json`` method will only load one data into 
the resources pool: it regnoise the object key "accounts" as 
a resource
::

    rk4 = ResourceKeeper()
    rk4.load_from_json("./accounts_object.json")
    res = rk4.get()
    pres.to_dict())        # {'res_id': 1, 'data': 'accounts'}


Customization
----------------
The ``ResourceKeeper`` consist of two parts: a map that stores all 
resources, and a set that maintains all available resources(id). 
Both the two key components can be customized by users. 

Poolmaps
++++++++++++
When a resource was added, an id was generated and the map storage 
maps the resource id to that resource data. By default, ``ResourceKeeper`` 
uses a python dict wrapper as the storage map. Users can make 
their own maps that meet their own needs, as long as their maps 
implementing three interfaces: ``get``, ``put``, and ``delete``. 

The three interfaces hehave the same like ``get``, ``__setitem__``, and 
``__del__`` of python dict. Users are suggested to examine and extend 
the base class ``reskeeper.poolmaps.PoolMapABC``. 
An example is the encapsulation of sqlite3 to be a map. It can 
be found in `reskeeper.poolmaps.SimpleSqliteMap <https://github.com/qige96/reskeeper/blob/master/reskeeper/poolmaps.py>`_.

Availsets
+++++++++++++
The other component is a set that maintains all ids of available 
resources. When users call ``rk.get()`` to apply for a resource, 
the ``avail_set`` pop out a ``res_id``, then the keeper return a copy 
of resource related to that id. When ``rk.release(res)`` is invoked, 
the keeper destroy the resource(actually the copy), and add the 
``res_id`` bake into ``avail_set``. Thus, an available set should 
implements four interaces: `contains`, ``add``, ``pop`` and ``delete``. 

Likewise, users are suggested to examine and extend the base class 
``reskeeper.availsets.AvailSetABC``. The default available set 
adopted by ``ResourceKeeper`` is `reskeeper.availsets.LinkedQueue <https://github.com/qige96/reskeeper/blob/master/reskeeper/availsets.py>`_ 
which is a linked list that has some queue and set features 
(not have same element, but in a queue order).


API
-------------


Core
+++++++
.. automodule:: reskeeper.core
    :members:


Poolmaps
++++++++++
.. automodule:: reskeeper.poolmaps
    :members:


Availsets
++++++++++++
.. automodule:: reskeeper.availsets
    :members:

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
