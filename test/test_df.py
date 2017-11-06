from flock.dataframe import DataFrameAsync
from pandas import DataFrame
import unittest


    
class TestDataFrame(unittest.TestCase):

    def funcHelper1(self, x):
        b = x ** 2
        return b

    def testDataFrame(self):
        dfA = DataFrameAsync()
        df = DataFrame({"a": list(range(1000)), "b": list(range(1000, 2000))})
        res = dfA.apply(df, self.funcHelper1)
        self.assertEqual(res.shape[0], 1000)
        self.assertEqual(res.shape[1], 2)

    def testDataFrameLambda(self):
        dfA = DataFrameAsync()
        df = DataFrame({"a": list(range(1000)), "b": list(range(1000, 2000))})
        res = dfA.apply(df, lambda v: ((v ** 2) / 20 * v) * v)
        self.assertEqual(res.shape[0], 1000)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
