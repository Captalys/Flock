from flock.base import BaseMultiProc
from flock.tools import split_chunks


class ListAsync(object):

    @classmethod
    def apply(cls, _list, function, chunksize=100, poolSize=5):
        """
        First we segmentat the orginal :mod:`List` in chunks, then the :func:`executeAsync()`
        will parallelize the function's operations on the segmented lists.

        :param list _list: Input List
        :param func fuction: Function to be applied on the list
        :param int chunksize: How many chunks the original list will be splitted
        :param int poolSize: Number of  pools of processes
        """

        bp = BaseMultiProc(poolSize=poolSize)
        res = bp.executeAsync(function, _list)
        return res
