from flockmp.dataframe import DataFrameAsync
from pandas import DataFrame
import pytest


class TestDataFrame(object):

    def funcHelper1(self, x):
        b = x ** 2
        return b

    def testDataFrame(self):
        df = DataFrame({"a": list(range(1000)), "b": list(range(1000, 2000))})
        res = DataFrameAsync.apply(df, lambda x: x ** 2)
        assert res.shape[0] == 1000
        assert res.shape[1] == 2

    def testDataFrameLambda(self):
        df = DataFrame({"a": list(range(1000)), "b": list(range(1000, 2000))})
        res = DataFrameAsync.apply(df, lambda v: ((v ** 2) / 20 * v) * v)
        assert res.shape[0] == 1000
