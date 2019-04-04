import unittest

from reskeeper import availsets

class StackAddTestCase(unittest.TestCase):

    def setUp(self):
        self.aq = availsets.ArrayStack()

    def test_add_head(self):
        self.aq.add(1)
        self.aq.add(2)
        self.aq.add(3)
        self.assertEqual(self.aq.stack_set[0], 1)
        self.assertEqual(self.aq.stack_set[1], 2)
        self.assertEqual(self.aq.stack_set[2], 3)


class StackPopTestCase(unittest.TestCase):

    def setUp(self):
        self.aq = availsets.ArrayStack()

    def test_pop_tail(self):
        self.aq.stack_set.append(1)
        self.aq.stack_set.append(2)
        self.aq.stack_set.append(3)
        self.assertEqual(self.aq.pop(), 3)
        self.assertEqual(self.aq.pop(), 2)
        self.assertEqual(self.aq.pop(), 1)
        self.assertEqual(len(self.aq.stack_set), 0)

    def test_pop_error_when_empty(self):
        with self.assertRaises(IndexError):
            self.aq.pop()
