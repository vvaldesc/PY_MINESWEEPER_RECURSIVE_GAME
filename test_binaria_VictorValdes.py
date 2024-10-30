from unittest import TestCase
from binaria_VictorValdes import binary_array_search
import numpy as np

a = np.arange(2)
b = np.arange(100)

class Test(TestCase):
    def test_binary_search_found(self):
        self.assertEqual(binary_array_search(a,1),1,"La prueba 1 ha fallado")
        self.assertEqual(binary_array_search(b,45),45,"La prueba 2 ha fallado")

    def test_binary_search_not_found(self):
        self.assertNotEqual(binary_array_search(b,200),False,"La prueba 3 ha fallado")
        self.assertNotEqual(binary_array_search(b,700),False,"La prueba 4 ha fallado")
