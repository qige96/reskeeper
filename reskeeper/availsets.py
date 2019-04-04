# coding: utf-8
"""
This module gives some AvailSet class for constructing avail_set
component. Also an abstract class is provided for customization. 
Developers are suggested to extend the class `AvailSetABC` 
and implements all its abstract methods.
"""

import abc


class AvailSetABC:
    """
    Abstract class for writing component `avail_set`.
    Developer should implement four functions: `contain`,
    `add` ,`pop` and `delete`.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def contain(self, item):
        """
        Check whether the set contains the given item.

        :param item: item to be checked
        :return: bool, return True if the set contains given item
        """
        pass
    
    @abc.abstractmethod
    def add(self, item):
        """
        Add an item ti the set. If there had has been an 
        identical item in the set, then do nothing.

        :param item: item to be added to the set
        """
        pass

    @abc.abstractmethod
    def pop(self):
        """
        Pop out an item from the set.
        Raise an IndexError if the set is empty.

        :return: item from the set
        """
        pass

    @abc.abstractmethod
    def delete(self, item):
        """
        delete an item from the set.
        Raise KeyError if the item not found.
        """
        pass


class ArrayStack(AvailSetABC):
    """
    A simple stack-like implementation of AvailSetABC, 
    inside is a python list.
    """
    def __init__(self):
        self.stack_set = list()
    
    def __len__(self):
        return len(self.stack_set)

    def contain(self, item):
        return (item in self.stack_set)

    def add(self, item):
        if self.contain(item):
            return
        self.stack_set.append(item)
    
    def pop(self):
        if len(self.stack_set) == 0:
            raise IndexError("ArrayStack is empty")
        return self.stack_set.pop()
    
    def delete(self, item):
        try:
            self.stack_set.remove(item)
        except ValueError:
            raise KeyError("res_id {0} not found".format(item))
            

class ArrayQueue(AvailSetABC):
    """
    A simple queue-like implementation of AvailSetABC, 
    inside is a python list.
    """
    def __init__(self):
        self.queue_set = list()

    def __len__(self):
        return self.queue_set.__len__()

    def contain(self, item):
        return (item in self.queue_set)

    def add(self, item):
        if self.contain(item):
            return
        self.queue_set.append(item)

    def pop(self):
        if len(self.queue_set) == 0:
            raise IndexError("ArrayQueue is empty")
        tmp = self.queue_set[0]
        del self.queue_set[0]
        return tmp

    def delete(self, item):
        try:
            self.queue_set.remove(item)
        except ValueError:
            raise KeyError("res_id {0} not found".format(item))
            

class LinkedQueue(AvailSetABC):
    """
    A simple queue-like implementation of AvailSetABC, 
    essentially a linked list.
    """
    class Node:
        def __init__(self, item):
            self.next = None
            self.prev = None 
            self.item = item

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def contain(self, item):
        ptr = self.head
        while ptr:
            if ptr.item == item:
                return True
            ptr = ptr.next
        return False

    def add(self, item):
        if self.contain(item):
            return
        node = self.Node(item)
        if self.size == 0:
            self.head = node
            self.tail = node
            self.size += 1
        else:
            self.head.prev = node
            node.next = self.head
            self.head = node
            self.size += 1
        
    def pop(self):
        if self.size == 0:
            raise IndexError("LinkedQueue is empty")
        if self.size == 1:
            item = self.tail.item
            self.head = None
            self.tail = None
            self.size -= 1
            return item
        else:
            item = self.tail.item
            self.tail.prev.next = None
            self.tail = self.tail.prev
            self.size -= 1
            return item


    def delete(self, item):
        ptr = self.head
        while ptr:
            if ptr.item == item:
                ptr.prev.next = ptr.next
                self.size -= 1
            ptr = ptr.next
        raise KeyError("res_id {0} not found".format(item))