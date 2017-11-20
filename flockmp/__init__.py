from flockmp.base import BaseMultiProc
from flockmp.utils import isIter
from flockmp.utils.logger import FlockLogger


class FunctionAsync(object):
    """
    :class:`FunctionAsync` is a class to apply and manage multiprocessing tasks within functions.
    """

    @classmethod
    def apply(cls, iterator, function, poolSize=5):
        """
        Method :func:`apply` executes a function asynchronously given an iterator.

        :param iter iterator: variable in which the function will be applied.
        :param func function: a function in which is desired to be ran multi-processed.

        Returns the list with the results of function(iterator).
        """
        logger = FlockLogger()
        bp = BaseMultiProc(poolSize=poolSize)

        if not isIter(iterator):
            logger.error("Variable `iterator` should be iterable.")
            return

        res = bp.executeAsync(function, iterator)
        logger.info("Successful execution of function {}".format(function.__name__))
        return res
