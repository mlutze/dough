import data
import unittest

class TestData(unittest.TestCase):
    
    def testRequireLock(self):
        d = data.Data("/tmp/test")
        with self.assertRaises(data.UnsafeOperation):
            d.get()