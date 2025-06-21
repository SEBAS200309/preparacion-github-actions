import unittest
from app import calcular_suma, calcular_producto

class TestCalculadora(unittest.TestCase):
    def test_suma(self):
        self.assertEqual(calcular_suma(2, 3), 5)
        self.assertEqual(calcular_suma(-1, 1), 0)
    
    def test_producto(self):
        self.assertEqual(calcular_producto(4, 5), 20)
        self.assertEqual(calcular_producto(0, 10), 0)

if __name__ == '__main__':
    unittest.main()