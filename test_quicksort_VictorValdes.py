from unittest import TestCase
import numpy as np
from  quicksort_VictorValdes import binary_array_sort

a = np.arange(10,-1,-1)
c = np.array([0, 0, 0, 0, 0])
d = np.array([-5, -2, -1, -4])

class Test(TestCase):
    def test_binary_array_sort(self):
        np.testing.assert_array_equal(binary_array_sort(c), np.array([0, 0, 0, 0, 0]), 'Error with test 1')
        np.testing.assert_array_equal(binary_array_sort(d), np.array([-5, -4, -2, -1]), 'Error with test 2')
        np.testing.assert_array_equal(binary_array_sort(a), np.arange(11), 'Error with test 3')