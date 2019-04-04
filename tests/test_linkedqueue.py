import unittest

from reskeeper import availsets

class QueueAddTestCase(unittest.TestCase):

    def setUp(self):
        self.lq = availsets.LinkedQueue()

    def test_add_head(self):
        self.lq.add(1)
        self.lq.add(2)
        self.lq.add(3)
        self.assertEqual(self.lq.head.item, 3)
        self.assertEqual(self.lq.head.next.item, 2)
        self.assertEqual(self.lq.tail.item, 1)


class QueuePopTestCase(unittest.TestCase):
    
    def setUp(self):
        self.lq = availsets.LinkedQueue()

    def test_pop_tail(self):
        self.lq.add(1)
        self.lq.add(2)
        self.lq.add(3)
        self.assertEqual(self.lq.pop(), 1)
        self.assertEqual(self.lq.pop(), 2)
        self.assertEqual(self.lq.pop(), 3)


    def test_pop_error_when_empty(self):
        with self.assertRaises(IndexError):
            self.lq.pop()
