# coding: utf-8
"""
docstring

"""

import copy
import csv
import json
from pprint import pprint

from reskeeper import poolmaps
from reskeeper import availsets
from reskeeper import utils


class Resource:
    """
    Wrapper for resource data
    """
    def __init__(self, res_id, data):
        self.res_id = res_id
        self.data = data

    def __str__(self):
        return "<res_id: {0}>".format(self.res_id)

    def __repr__(self):
        return "<res_id: {0}>".format(self.res_id)

    def destroy(self):
        """
        Destroy the resource
        """
        self.res_id = None
        self.data = None
    
    def to_dict(self):
        """
        Return a python dict wrapping resource id and resource data
        """
        return {
            "res_id": self.res_id,
            "data": self.data
        }


class ResourceKeeper:
    """
    Resource manager that provide book keeping functionality
    """

    def __init__(self, resources=None, pool_map=None, avail_set=None):
        """
        Instanciate a resource manager
        """
        if pool_map:
            self.pool = pool_map
        else:
            self.pool = poolmaps.DictMap()

        if avail_set:
            self.available = avail_set
        else:
            self.available = availsets.ArrayQueue()

        self.size = 0
        self.avail_num = 0
        self._max_id = 0
        if resources:
            self.load(resources)

    def get(self):
        """"
        Get a resource from resource pool.

        :return: a random resource
        """
        if self.avail_num == 0:
            return None
        res_id = self.available.pop()
        data = copy.deepcopy(self.pool.get(res_id))
        self.avail_num -= 1
        return Resource(res_id, data)

    def release(self, resourse):
        """
        Release a resource.
        Note: after releasing, user lose the resource.

        :param resource: Resource, the resource to be released 
        """
        if not self.available.contain(resourse.res_id):
            self.available.add(resourse.res_id)
            self.avail_num += 1
        resourse.destroy()

    def add(self, data):
        """
        Add data to the resources pool

        :param resource: obj, the resource to be added
        """
        self._max_id += 1
        self.pool.put(self._max_id, data)
        self.available.add(self._max_id)
        self.size += 1
        self.avail_num += 1

    def remove(self, resource):
        """
        Remove the resource from the resources pool
       
        :param resource: Resource, the resource to be removed
        """
        try:
            self.available.delete(resource.res_id)
            self.pool.delete(resource.res_id)
            self.size -= 1
            self.avail_num -= 1
        except KeyError:
            raise KeyError("No resource with res_id: " + str(resource.res_id))

    def load(self, resources_data):
        """
        Load a batch of data into the resources pool

        :param resources_data: should be iterable
        """
        for data in resources_data:
            self.add(data)

    def load_csv_file(self, file_dir):
        """
        Load a batch of data from given csv file. 

        :param file_dir: str, directory where the csv file located
        """
        with open(file_dir, "r") as f:
            csv_iterator = csv.reader(f)
            self.load(csv_iterator)

    def load_json_file(self, file_dir):
        """
        Load a batch of data from given json file. 

        :param file_dir: str, directory where the json file located
        """
        with open(file_dir, "r") as f:
            json_data = json.load(f)
            self.load(json_data)