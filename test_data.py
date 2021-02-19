import data
import unittest

class TestData(unittest.TestCase):
    
    def test_require_lock(self):
        d = data.Data("/tmp/test")
        with self.assertRaises(data.UnsafeOperation):
            d.get()