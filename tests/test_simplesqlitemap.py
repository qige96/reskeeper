import unittest

from reskeeper import poolmaps

class GetitemTestCase(unittest.TestCase):

    def setUp(self):
        self.map = poolmaps.SimpleSqliteMap(":memory:")

    def tearDown(self):
        self.map.conn.close()

    def test_get(self):
        self.map.conn.execute("insert into pool values(1, '123')")
        self.map.conn.commit()
        self.assertEqual('123', self.map.get(1))
    
    def test_get_none(self):
        self.assertIsNone(self.map.get(1000))


class PutitemTestCase(unittest.TestCase):

    def setUp(self):
        self.map = poolmaps.SimpleSqliteMap(":memory:")

    def tearDown(self):
        self.map.conn.close()

    def test_put(self):
        self.map.put(1, "123")
        cur = self.map.conn.cursor()
        record = cur.execute("select * from pool").fetchone()
        self.assertTupleEqual(record, (1, "123"))
        
    def test_put_not_str_error(self):
        with self.assertRaises(TypeError):
            self.map.put(1, 123)
        with self.assertRaises(TypeError):
            self.map.put(1, [123])
        with self.assertRaises(TypeError):
            self.map.put(1, map)
    
    def test_put_id_exist(self):
        self.map.conn.execute("insert into pool values(1,'123')")
        data = self.map.conn.execute(
            "select data from pool where res_id=1;").fetchone()[0]
        self.assertEqual('123', data)

        self.map.conn.commit()
        self.map.put(1, 'abc')
        data = self.map.conn.execute(
            "select data from pool where res_id=1;").fetchone()[0]
        self.assertEqual('abc', data)


class DeleteTestCase(unittest.TestCase):

    def setUp(self):
        self.map = poolmaps.SimpleSqliteMap(":memory:")

    def tearDown(self):
        self.map.conn.close()

    def test_delete(self):
        self.map.conn.execute("insert into pool values(1,'123')")
        data = self.map.conn.execute(
            "select data from pool where res_id=1;").fetchone()[0]
        self.assertEqual('123', data)
        self.map.delete(1)
        data = self.map.conn.execute(
            "select data from pool where res_id=1;").fetchone()
        self.assertIsNone(data)

    def test_delete_not_exist(self):
        self.map.conn.execute("insert into pool values(1,'123')")
        data = self.map.conn.execute(
            "select data from pool where res_id=1;").fetchone()[0]
        self.assertEqual('123', data)
        self.map.delete(1)
        with self.assertRaises(KeyError):
            self.map.delete(1)
            self.map.delete(1)
        data = self.map.conn.execute(
            "select data from pool where res_id=1;").fetchone()
        self.assertIsNone(data)  

        with self.assertRaises(KeyError):
            self.map.delete(10)
            self.map.delete(10)
        data = self.map.conn.execute(
            "select data from pool where res_id=10;").fetchone()
        self.assertIsNone(data)    

        
