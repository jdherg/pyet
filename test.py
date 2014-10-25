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

    def test_add(self):
        self.stack.add()
        self.assertEqual([1, 2, 3, 9], self.stack)

        self.stack.add()
        self.stack.add()
        self.stack.add()
        self.assertEqual([15], self.stack)

        self.stack.add()
        self.assertEqual([15], self.stack)

    def test_subtract(self):
        self.stack.subtract()
        self.assertEqual([1, 2, 3, -1], self.stack)

        self.stack.subtract()
        self.stack.subtract()
        self.stack.subtract()
        self.assertEqual([3], self.stack)

        self.stack.subtract()
        self.assertEqual([3], self.stack)

    def test_multiply(self):
        self.stack.multiply()
        self.assertEqual([1, 2, 3, 20], self.stack)

        self.stack.multiply()
        self.stack.multiply()
        self.stack.multiply()
        self.assertEqual([120], self.stack)

        self.stack.multiply()
        self.assertEqual([120], self.stack)

    def test_divide(self):
        self.stack.divide()
        self.assertEqual([1, 2, 3, 0], self.stack)

    def test_mod(self):
        self.stack.mod()
        self.assertEqual([1, 2, 3, 4], self.stack)

    def test_not(self):
        self.stack.logical_not()
        self.assertEqual([1, 2, 3, 4, 0], self.stack)

        self.stack.logical_not()
        self.assertEqual([1, 2, 3, 4, 1], self.stack)

    def test_greater(self):
        self.stack.greater()
        self.assertEqual([1, 2, 3, 0], self.stack)

        self.stack.greater()
        self.assertEqual([1, 2, 1], self.stack)

    def test_duplicate(self):
        self.stack.duplicate()
        self.assertEqual([1, 2, 3, 4, 5, 5], self.stack)

    def test_pos_roll(self):
        self.stack._roll_helper(2, 2)
        self.assertEqual([1, 2, 3, 4, 5], self.stack)

        self.stack._roll_helper(1, 2)
        self.assertEqual([1, 2, 3, 5, 4], self.stack)

        self.stack._roll_helper(4, 3)
        self.assertEqual([1, 2, 4, 3, 5], self.stack)

    def test_neg_roll(self):
        self.stack._roll_helper(-2, 2)
        self.assertEqual([1, 2, 3, 4, 5], self.stack)

        self.stack._roll_helper(-1, 2)
        self.assertEqual([1, 2, 3, 5, 4], self.stack)

        self.stack._roll_helper(-4, 3)
        self.assertEqual([1, 2, 5, 4, 3], self.stack)

if __name__ == '__main__':
    unittest.main()
