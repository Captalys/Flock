from flockmp.base import BaseMultiProc
from flockmp.utils import split_chunks
from pandas import concat


class DataFrameAsync(object):

    @classmethod
    def applyInRows(cls, args):
        """
        :func:`Applyinrows` method takes a dataframe and the function to be applied at as arguments.
        It stores every row of the dataframe in a list list.
        Through :func:`BaseMultiProc.executeAsync()` method, it processes the fuctions at each element of the list (row) in parallel calling different processes

        Returns a Dataframe by concating the processed rows.

        :param tuple args: Function that will be applied at the Dataframe
        """
        func, block_df = args
        _df2 = block_df.copy()
        list_rows = []

        for i in range(len(_df2)):
            list_rows.append(_df2.iloc[i:i + 1])

        bp2 = BaseMultiProc()
        res2 = bp2.executeAsync(func, list_rows)
        res2 = concat(res2)

        return res2

    @classmethod
    def apply(cls, dataframe, function, style="row-like",
              chunksize=100, poolSize=5):
        """
        First we segmentat the orginal :mod:`DataFrame` in chunks, then the :func:`executeAsync()` will parallelize the function's operations on the segmented dataframes.
        There two options for the way it will operate, as `row-like` or `block-like`.

        :param DataFrame dataframe: Input Dataframe
        :param func fuction: Function to be applied on the dataframe
        :param int chunksize: How many chunks the original dataframe will be splitted
        :param int poolSize: Number of  pools of processes
        :param str style: if "row-like" :func:`function` will be applied in row-by-row, otherwise it will be applied in :mod:`DataFrame` chunks.
        """
        _df = dataframe.copy()
        iterator = split_chunks(_df, _type="dataframe", size=chunksize)

        bp = BaseMultiProc(poolSize=poolSize)

        if style == "row-like":
            iterator = [(function, el) for el in iterator]
            res = bp.executeAsync(cls.applyInRows, iterator)

        elif style == "block-like":
            res = bp.executeAsync(function, iterator)

        else:
            raise Exception("Style-type not supported")

        res = concat(res)
        res = res.sort_index()

        return res
