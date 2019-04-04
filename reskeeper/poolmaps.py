# coding: utf-8
"""
This module gives some PoolMap class for constructing pool_map
component. Also an abstract class is provided for customization. 
Developers are suggested to extend the class `PoolMapABC` 
and implements all its abstract methods.
"""

import sqlite3
import abc


class PoolMapABC:
    """
    Abstract class for writing component `pool_map`.
    Developer should implement three functions: `get`,
    `add` and `pop`
    """
    __metaclass__ =  abc.ABCMeta

    @abc.abstractmethod
    def get(self, key):
        """
        Return an item by the given key. Return None if the key doesn't exist.

        :return: item
        """
        pass
    
    @abc.abstractmethod
    def put(self, key, val):
        """
        Store the key and the related item. Overwrite the value if
        the key exist.
        """
        pass

    @abc.abstractmethod
    def delete(self, key):
        """
        Delete the key and the related item. 
        Raise KeyError if the key doesn't exist.
        """
        pass


class DictMap(PoolMapABC):
    """
    Wrapper of python dict.
    """
    def __init__(self):
        self.map = dict()

    def get(self, key):
        return self.map.get(key)

    def put(self, key, val):
        self.map[key] = val

    def delete(self, key):
        del self.map[key]


class SimpleSqliteMap(PoolMapABC):
    """
    Sqlite storage for resources. Note that data to be stored can
    only be strings.
    """
    
    def __init__(self, db_path="./reskeeper.db"):
        self.conn = sqlite3.connect(db_path) 
        self.conn.execute(
            "create table pool(res_id int primary key, data text);")
        self.conn.commit()

    def get(self, key):
        cur = self.conn.cursor()
        cur.execute(
            "select data from pool where res_id={0}".format(key))
        data = cur.fetchone()
        if data:
            data = data[0]
        cur.close()
        return data

    def put(self, key, val):
        if not isinstance(val, str):
            raise TypeError('Argument "val" shoule be str type')
        try:
            self.conn.execute(
                'insert into pool values({0}, "{1}")'.format(key, val))
        except sqlite3.IntegrityError:
            self.conn.execute(
                'update pool set data="{0}" where res_id={1}'.format(val,key))
        finally:
            self.conn.commit()

    def delete(self, key):
        if len(self.conn.execute('select res_id from pool where res_id={0}'
            .format(key)).fetchall()) == 0:
            raise KeyError("sqlite has no record with res_id: " + str(key))
        self.conn.execute(
            "delete from pool where res_id={0}".format(key))
        self.conn.commit()

    def close(self):
        self.conn.close()