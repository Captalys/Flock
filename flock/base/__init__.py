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


class NoDaemonProcess(Process):
    """
    :class:`NoDaemonProcess` is that ensure the process' daemon flag is false.
    
    When a process exits, it attempts to terminate all of its daemonic child processes.
    
    It inheritates the Process method from `multiprocessing`
    Parameters:
        Process: method inherited from `multiprocessing` package
    """
   
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


class FlockPool(Pool):
    """
    :class:`FlockPool` inheritates the Pool method form `multiprocessing` package. It settles the pool size and
    context that will be used to use the function asynchronally.
        Parameters:
        Pool: method inherited from `multiprocessing` package
    """
    Process = NoDaemonProcess


class BaseMultiProc(object):
    """
    :class:`BaseMultiProc` is a class to apply and manage multiprocessing tasks within fucntions.
    Parameters:
        poolSize: amount of resources set to be processed the same time (`default` = 5)\n
        timeOutError:  degree of tolerance for waiting a process to end (`default` = 50)\n
        context: way of starting a process (depends os the platform). It can be "spawn", "fork" or "forkserver" (`default`="spawn")
    """

    def __init__(self, poolSize=5, timeOutError=50, context="spawn"):
        self.poolSize = poolSize
        self.timeOutError = timeOutError
        self.context = context
        self.results = []

    def getResults(self, result):
        """
        :func:`getResults` append results obtained from functions asynchronally.
        Parameters: 
            result: results calculated from the function
        """
        self.results.append(result)

    def logErrors(self, localQueue):
        """
        :func:`logErrors` takes as argument the queue to be processed and assess if the process has timed-out
        Parameters:
            localQueue: list of process to be executed 
        """
        for asyncRes in localQueue:
            try:
                retQ = asyncRes.get(timeout=self.timeOutError)
                del retQ
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    @classmethod
    def dillEncoded(cls, payload):
        """
        :func:`dillEncoded` encodes the already serialized `function` and `argument`
        Parameter:
            payload: serialized function and argument
        """
        fun, args = dill.loads(payload)
        return fun(*args)

    @classmethod
    def customApplyAsync(cls, pool, fun, args, callback):
        """
        :func:`customApplyAsync` 
        Parameters:
            pool: parameters such as poll size and context.
            fun: a function in which is desired to be ran multiprocessed and asynchronally
            args: variables to be applied to the function
            callback: it called, if supplied, when the function is complete
        """
        payload = dill.dumps((fun, args))
        return pool.apply_async(cls.dillEncoded, (payload,), callback=callback)

    def computeFunc(self, childCon, function, iterator):
        """
        :func:`computeFunc` recieves the function and iterator used in :func:`executeAsync` together with an endpoint for the
        processor. It calculates the results of the function, for each iterator and sets queue of process to be executed.
        Parameters:
            childCon: endpoint conection\n
            function: a function in which is desired to be ran multiprocessed and asynchronally\n
            iterator: variable in wich the function will be applied
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
        Parameters:
            function: a function in which is desired to be ran multiprocessed and asynchronally\n
            iterator: variable in wich the function will be applied
        
        Returns the result of the function given a set of arguments of that function.
        """
        parentCon, childCon = Pipe()
        parentProcess = Process(target=self.computeFunc, args=(childCon, function,  iterator))
        parentProcess.daemon = False
        parentProcess.start()
        res = parentCon.recv()
        parentProcess.join()
        return res


# def funcHelper1(a):
#     from flock.base.database import SqlCon
#     try:
#         engine = SqlCon.mysql_engine("varejo")
#         conn = engine.connect()
#         b = (a ** 2)
#         return b
#     except Exception as e:
#         raise e

# if __name__ == '__main__':
#     bp = BaseMultiProc()
#     iterator = list(range(100))
#     res = bp.executeAsync(funcHelper1, iterator)
#     print(res)
