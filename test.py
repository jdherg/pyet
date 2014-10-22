import pyet
import unittest


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = pyet.PietStack([1, 2, 3, 4, 5])

    def test_top(self):
        self.assertEqual(5, self.stack.top())

    def test_push(self):
        self.stack.push(1)
        self.assertEqual(1, self.stack.top())

    def test_pop2(self):
        self.assertEqual((5, 4), self.stack.pop2())

if __name__ == '__main__':
    unittest.main()
