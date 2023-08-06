import unittest

from kanina.calculator import *


class TestSum(unittest.TestCase):
    def test_sum(self):
        """
        Test that it can sum a list of integers
        """
        c = Calculator()
        data = [1, 2, 3]
        for num in data:
            c.add(num)
        result = c.cval()
        self.assertEqual(result, 6)

    def test_sub(self):
        """
        Test that it can subtract a list of integers
        """
        c = Calculator()
        data = [1, 2, 3]
        for num in data:
            c.sub(num)
        result = c.cval()
        self.assertEqual(result, -6)

    def test_reset(self):
        """
        Test that it sets to 0
        """
        c = Calculator()
        data = [1, 2, 3]
        for num in data:
            c.sub(num)
        c.reset()
        result = c.cval()
        self.assertEqual(result, 0)

    def test_mult(self):
        """
        Test that it multiplies correctly
        """
        c = Calculator(1)
        data = [1, 2, 3, -4]
        for num in data:
            c.mult(num)
        result = c.cval()
        self.assertEqual(result, -24)

    def test_div(self):
        """
        Test that it divides correctly
        """
        c = Calculator(100)
        data = [1, 2, 10]
        for num in data:
            c.div(num)
        result = c.cval()
        self.assertEqual(result, 5)

    def test_pow(self):
        """
        Test that raises by power correctly
        """
        c = Calculator(2)
        self.assertEqual(c.pow(3), 8)
        c = Calculator(-2)
        self.assertEqual(c.pow(5), -32)

    def test_1_cannot_add_int_and_str(self):
        """
        Test that ValueError is raised when trying to apply even root operation on negative number
        """
        with self.assertRaises(ValueError):
            c = Calculator(-16)
            c.root(4)

    def test_root(self):
        """
        Test that calculates root correctly
        """
        c = Calculator(16)
        self.assertEqual(c.root(2), 4.)
        c = Calculator(-27)
        self.assertEqual(c.root(3), -3.)

if __name__ == '__main__':
    unittest.main()