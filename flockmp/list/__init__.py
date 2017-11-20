from flockmp.base import BaseMultiProc


class ListAsync(object):

    @classmethod
    def apply(cls, _list, function, poolSize=5):
        """
        First we segmentat the orginal :mod:`List` in chunks, then the :func:`executeAsync()`
        will parallelize the function's operations on the segmented lists.

        :param list _list: Input List
        :param func fuction: Function to be applied on the list
        :param int poolSize: Number of  pools of processes
        """

        bp = BaseMultiProc(poolSize=poolSize)
        res = bp.executeAsync(function, _list)
        return res
