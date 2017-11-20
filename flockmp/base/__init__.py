"""
.. module:: base
   :platform: Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Wanderson Ferreira <wanderson.ferreira@captalys.com.br>

"""

import sys
import dill
from multiprocessing import Process, Pipe, get_context
from multiprocessing.pool import Pool
from flockmp.utils.logger import FlockLogger


class NoDaemonProcess(Process):
    """
    :class:`NoDaemonProcess` is that ensure the process' daemon flag is false.

    When a process exits, it attempts to terminate all of its daemonic child processes.

    It inheritates the Process method from `multiprocessing`

    :param Process Process: method inherited from `multiprocessing` package
    """

    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


class FlockPool(Pool):
    """
    :class:`FlockPool` inheritates the Pool method from :mod:`multiprocessing` module. It settles the pool size and
    context that will be used to use the function asynchronally.

    Parameters
    ----------
        Pool: method inherited from :mod:`multiprocessing` module
    """
    Process = NoDaemonProcess


class BaseMultiProc(object):
    """
    :class:`BaseMultiProc` is a class to apply and manage multiprocessing tasks within fucntions.

    :param int poolSize: amount of resources set to be processed the same time (`default` = 5)\n
    :param int timeOutError:  degree of tolerance for waiting a process to end (`default` = 50)\n
    :param str context: way of starting a process (depends os the platform). It can be "spawn", "fork" or "forkserver" (`default`="spawn")
    """

    def __init__(self, poolSize=5, timeOutError=50, context="spawn"):
        self.poolSize = poolSize
        self.timeOutError = timeOutError
        self.context = context
        self.results = []

    def getResults(self, result):
        """
        :func:`getResults` append results obtained from functions asynchronally.

        :param list result: results calculated from the function
        """
        self.results.append(result)

    def logErrors(self, localQueue):
        """
        :func:`logErrors` takes as argument the queue to be processed and assess if the process has timed-out

        :param list localQueue: list of process to be executed
        """
        for asyncRes in localQueue:
            try:
                retQ = asyncRes.get(timeout=self.timeOutError)
                del retQ
            except Exception as e:
                fl = FlockLogger()
                fl.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                print("Some error occur - Check the logs.")

    @classmethod
    def dillEncoded(cls, payload):
        """
        :func:`dillEncoded` encodes the already serialized `function` and `argument`
        :param dict payload: serialized function and argument
        """
        fun, args = dill.loads(payload)
        return fun(*args)

    @classmethod
    def customApplyAsync(cls, pool, fun, args, callback):
        """
        :func:`customApplyAsync`

        :param Pool pool: parameters such as poll size and context.
        :param func fun: a function in which is desired to be ran multiprocessed and asynchronally
        :param tuple args: variables to be applied to the function
        :param func callback: it called, if supplied, when the function is complete
        """
        payload = dill.dumps((fun, args))
        return pool.apply_async(cls.dillEncoded, (payload,), callback=callback)

    def computeFunc(self, childCon, function, iterator):
        """
        :func:`computeFunc` recieves the function and iterator used in :func:`executeAsync` together with an endpoint for the
        processor. It calculates the results of the function, for each iterator and sets queue of process to be executed.

        :param Pipe childCon: endpoint conection\n
        :param func function: a function in which is desired to be ran multiprocessed and asynchronally\n
        :param iter iterator: variable in wich the function will be applied
        """
        pool = FlockPool(self.poolSize, context=get_context(self.context))
        localQueue = []
        for it in iterator:
            asyncRes = self.customApplyAsync(pool, function, args=(it,), callback=self.getResults)
            localQueue.append(asyncRes)

        pool.close()
        pool.join()

        self.logErrors(localQueue)
        childCon.send(self.results)

    def executeAsync(self, function, iterator):
        """
        Method :func:`executeAsync` executes a function asynchronally, given a set of iterators.

        :param func function: a function in which is desired to be ran multiprocessed and asynchronally\n
        :param iter iterator: variable in wich the function will be applied

        Returns the result of the function given a set of arguments of that function.
        """
        parentCon, childCon = Pipe()
        parentProcess = Process(target=self.computeFunc, args=(childCon, function, iterator))
        parentProcess.daemon = False
        parentProcess.start()
        res = parentCon.recv()
        parentProcess.join()
        return res
