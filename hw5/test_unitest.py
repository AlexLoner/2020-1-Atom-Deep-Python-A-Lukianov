import unittest
import mock
import function


class TestFunc(unittest.TestCase):


    def test_wrong_input(self):
        self.assertRaises(AssertionError, function.func, 'string')

    def test_wrong_list_contains(self):
        self.assertRaises(AssertionError, function.func, [1, 2, 3, ''])

    def test_output(self):
        array = [2, 1, 5, 7]
        self.assertEqual(function.func(array), [35, 70, 14, 10])

    @mock.patch('math.prod', return_value=([6, 6, 6]))
    def test_output_mock1(self, func):
        self.assertEqual(func([2, 3, 6]), [6, 6, 6])

    @mock.patch('function.func', return_value=([6, 1, 6]))
    def test_output_mock2(self, func):
        self.assertEqual(func([1, 6, 1]), [6, 1, 6])

    @mock.patch('math.prod', return_value=([6, 1, 6]))
    def test_output_mock3(self, func):
        self.assertEqual(func([1, 6, 1]), [6, 1, 6])
