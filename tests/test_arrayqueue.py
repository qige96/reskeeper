import unittest

from reskeeper import availsets

class QueueAddTestCase(unittest.TestCase):

    def setUp(self):
        self.aq = availsets.ArrayQueue()

    def test_add_head(self):
        self.aq.add(1)
        self.aq.add(2)
        self.aq.add(3)
        self.assertEqual(self.aq.queue_set[0], 1)
        self.assertEqual(self.aq.queue_set[1], 2)
        self.assertEqual(self.aq.queue_set[2], 3)


class QueuePopTestCase(unittest.TestCase):

    def setUp(self):
        self.aq = availsets.ArrayQueue()

    def test_pop_tail(self):
        self.aq.queue_set.append(1)
        self.aq.queue_set.append(2)
        self.aq.queue_set.append(3)
        self.assertEqual(self.aq.pop(), 1)
        self.assertEqual(self.aq.pop(), 2)
        self.assertEqual(self.aq.pop(), 3)
        self.assertEqual(len(self.aq.queue_set), 0)

    def test_pop_error_when_empty(self):
        with self.assertRaises(IndexError):
            self.aq.pop()
