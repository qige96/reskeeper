import unittest
import os

from reskeeper.core import Resource, ResourceKeeper


class GetTestCase(unittest.TestCase):

    def setUp(self):
        self.keeper = ResourceKeeper()

    def test_get_simple_res(self):
        self.keeper.pool.put(1, 1)
        self.keeper.available.add(1)
        self.keeper.size += 1
        self.keeper.avail_num += 1
        self.keeper.pool.put(2, 2)
        self.keeper.available.add(2)
        self.keeper.size += 1
        self.keeper.avail_num += 1
        self.assertEqual(self.keeper.size, 2)
        self.assertEqual(self.keeper.avail_num, 2)
        res1 = self.keeper.get()
        res2 = self.keeper.get()
        self.assertEqual(self.keeper.size, 2)
        self.assertEqual(self.keeper.avail_num, 0)
        self.assertDictEqual(res1.to_dict(), {"res_id":1, "data": 1})
        self.assertDictEqual(res2.to_dict(), {"res_id":2, "data": 2})

    def test_get_complex_res(self):
        self.keeper.pool.put(3, {"func":sum, "tuple":("123", 123)})
        self.keeper.available.add(3)
        self.keeper.avail_num += 1
        self.keeper.size += 1

        self.keeper.pool.put(6, {"func":max, "tuple":("456", 456)})
        self.keeper.available.add(6)
        self.keeper.avail_num += 1
        self.keeper.size += 1

        self.assertEqual(self.keeper.size, 2)
        self.assertEqual(self.keeper.avail_num, 2)
        res1 = self.keeper.get()
        res2 = self.keeper.get()
        self.assertEqual(self.keeper.size, 2)
        self.assertEqual(self.keeper.avail_num, 0)
        self.assertDictEqual(res1.to_dict(), 
            {"res_id":3, "data": {"func":sum, "tuple":("123", 123)}})
        self.assertDictEqual(res2.to_dict(),
            {"res_id":6, "data": {"func":max, "tuple":("456", 456)}})

    def test_get_empty(self):
        self.keeper.pool.put(1, 1)
        self.keeper.available.add(1)
        self.keeper.avail_num += 1

        res1 = self.keeper.get()
        res2 = self.keeper.get()
        self.assertIsNone(res2)


class ReleaseTestCase(unittest.TestCase):

    def setUp(self):
        self.keeper = ResourceKeeper()

    def test_release(self):
        self.keeper.pool.put(1, "res1")
        self.assertEqual(self.keeper.avail_num, 0)
        self.assertFalse(self.keeper.available.contain(1))
        res = Resource(1, "res1")
        self.keeper.release(res)
        self.assertEqual(self.keeper.avail_num, 1)
        self.assertTrue(self.keeper.available.contain(1))
        self.assertIsNone(res.res_id)
        self.assertIsNone(res.data)

    def test_release_repeatedly(self):
        self.keeper.pool.put(1, "res1")
        self.assertEqual(self.keeper.avail_num, 0)
        self.assertFalse(self.keeper.available.contain(1))
        res = Resource(1, "res1")
        res2 = Resource(1, "res1")
        res3 = Resource(1, "res1")
        self.keeper.release(res)
        self.keeper.release(res2)
        self.keeper.release(res3)
        self.assertEqual(self.keeper.avail_num, 1)
        self.assertTrue(self.keeper.available.contain(1))
        self.assertIsNone(res.res_id)
        self.assertIsNone(res.data)



class AddTestCase(unittest.TestCase):

    def setUp(self):
        self.keeper = ResourceKeeper()

    def test_add_simple_res(self):
        self.keeper.add("res_str1")
        self.assertIn("res_str1", self.keeper.pool.get(1))
        self.assertTrue(self.keeper.available.contain(1))
        self.assertEqual(self.keeper.size, 1)
        self.assertEqual(self.keeper.avail_num, 1)

class RemoveTestCase(unittest.TestCase):

    def setUp(self):
        self.keeper = ResourceKeeper()

    def test_remove(self):
        self.keeper.pool.put(100, 100)
        self.keeper.size += 1

        self.keeper.remove(Resource(100, 100))
        self.assertEqual(self.keeper.size, 0)
        self.assertEqual(self.keeper.avail_num, 0)
        self.assertIsNone(self.keeper.pool.get(100))

    def test_remove_not_exist_res(self):
        with self.assertRaises(KeyError):
            self.keeper.remove(Resource(45454, "fsaf"))

class LoadTestCase(unittest.TestCase):

    def setUp(self):
        self.keeper = ResourceKeeper()

    def test_load_list(self):
        iterable = ["100", "200", "300"]
        self.keeper.load(iterable)
        self.assertEqual(self.keeper.size, 3)
        self.assertEqual(self.keeper.avail_num, 3)

    def test_load_dict(self):
        iterable = {
            "proxy1":{"host":"127.0.0.1", "port":"8000"},
            "proxy2":{"host":"127.0.0.3", "port":"8000"},
            "proxy3":{"host":"127.0.0.1", "port":"8001"},
        }
        self.keeper.load(iterable)
        self.assertEqual(self.keeper.size, 3)
        self.assertEqual(self.keeper.avail_num, 3)

class LoadFileTestCase(unittest.TestCase):

    def setUp(self):
        self.keeper = ResourceKeeper()

    def test_load_csv_file(self):
        file_dir = os.path.join(os.path.dirname(__file__), "asset.csv")
        self.keeper.load_csv_file(file_dir)
        self.assertEqual(self.keeper.size, 3)
        self.assertEqual(self.keeper.avail_num, 3)

    def test_load_json_file(self):
        file_dir = os.path.join(os.path.dirname(__file__), "asset.json")
        self.keeper.load_json_file(file_dir)
        self.assertEqual(self.keeper.size, 3)
        self.assertEqual(self.keeper.avail_num, 3)


if __name__ == '__main__':
    unittest.main()