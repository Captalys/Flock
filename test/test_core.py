from flock.core import applyAsync
from pandas import DataFrame
import unittest


    
class TestCore(unittest.TestCase):

    def funcHelper1(self, x):
        b = x ** 2
        return b

    def testDataFrame(self):
        df = DataFrame({"a": list(range(1000)), "b": list(range(1000, 2000))})
        res = applyAsync(df, self.funcHelper1)
        self.assertEqual(res.shape[0], 1000)
        self.assertEqual(res.shape[1], 2)

    def testDataFrameLambda(self):
        df = DataFrame({"a": list(range(1000)), "b": list(range(1000, 2000))})
        res = applyAsync(df, lambda v: ((v ** 2) / 20 * v) * v)
        self.assertEqual(res.shape[0], 1000)

    def testList(self):
        size = 1200
        _input = list(range(size))
        res = applyAsync(_input, lambda x: x ** 0.5)
        self.assertEqual(len(res), size)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
