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
    TODO: Docstring completa da classe
    """
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


class FlockPool(Pool):
    """
    TODO: Docstring completa da classe
    """
    Process = NoDaemonProcess


class BaseMultiProc(object):
    """
    TODO: Docstring completa da classe
    """

    def __init__(self, poolSize=5, timeOutError=50, context="spawn"):
        self.poolSize = poolSize
        self.timeOutError = timeOutError
        self.context = context
        self.results = []

    def getResults(self, result):
        """
        TODO: Docstring completa do metodo
        """
        self.results.append(result)

    def logErrors(self, localQueue):
        """
        TODO: Docstring completa do metodo
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
        TODO: Docstring completa do metodo
        """
        fun, args = dill.loads(payload)
        return fun(*args)

    @classmethod
    def customApplyAsync(cls, pool, fun, args, callback):
        """
        TODO: Docstring completa do metodo
        """
        payload = dill.dumps((fun, args))
        return pool.apply_async(cls.dillEncoded, (payload,), callback=callback)

    def computeFunc(self, childCon, function, iterator):
        """
        TODO: Docstring completa do metodo
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
        TODO: Docstring completa do metodo
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
