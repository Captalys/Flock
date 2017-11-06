from flock.base import BaseMultiProc
from flock.tools import split_chunks
from pandas import concat


class DataFrameAsync(object):

    def __init__(self, poolSize=5, poolSizeRows=10):
        self.function = None
        self.poolSize = poolSize
        self.poolSizeRows = poolSizeRows

    def applyInRows(self, block_df):
        _df2 = block_df.copy()
        list_rows = []

        for i in range(len(_df2)):
            list_rows.append(_df2.iloc[i:i+1])

        bp2 = BaseMultiProc(poolSize=self.poolSizeRows)
        res2 = bp2.executeAsync(self.function, list_rows)
        res2 = concat(res2)
        return res2

    def apply(self, dataframe, function, style="row-like", chunksize=100):
        _df = dataframe.copy()
        iterator = split_chunks(_df, _type="dataframe", size=chunksize)

        bp = BaseMultiProc(poolSize=self.poolSize)

        if style == "row-like":
            self.function = function
            res = bp.executeAsync(self.applyInRows, iterator)

        elif style == "block-like":
            res = bp.executeAsync(function, iterator)

        else:
            raise Exception("Style-type not supported")

        res = concat(res)
        res = res.sort_index()
        return res
