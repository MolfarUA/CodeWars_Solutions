import unittest

def opposite (number):
    return number * -1

class TestOpposite (unittest.TestCase):
    
    def test_opposite (self):
        self.assertEqual (opposite (1), -1)

if __name__ == '__main__':
    unittest.main()
