import sys
import dill
from multiprocessing import Process, Pipe, Pool, Manager, Queue, Value, get_context
from multiprocessing.managers import BaseManager

class BaseMultiProc(object):
    """Documentation for BaseMultiProc

    """

    def __init__(self, poolSize=10, timeOutError=5):
        self.poolSize = poolSize
        self.timeOutError = timeOutError
        self.results = []

    def getResults(self, result):
        self.results.append(result)

    def logErrors(self, localQueue):
        for asyncRes in localQueue:
            try:
                retQ = asyncRes.get(timeout=self.timeOutError)
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    @classmethod
    def dillEncoded(cls, payload):
        fun, args = dill.loads(payload)
        return fun(*args)

    @classmethod
    def customApplyAsync(cls, pool, fun, args, callback):
        payload = dill.dumps((fun, args))
        return pool.apply_async(cls.dillEncoded, (payload,), callback=callback)
    
    def computeFunc(self, childCon, function, iterator):
        ctx = get_context("spawn")
        pool = ctx.Pool(self.poolSize)
        localQueue = []
        for it in iterator:
            asyncRes = self.customApplyAsync(pool, function, args=(it,), callback=self.getResults)
            localQueue.append(asyncRes)
            
        pool.close()
        pool.join()
        
        self.logErrors(localQueue)
        childCon.send(self.results)


    def executeAsync(self, function, iterator):
        parentCon, childCon = Pipe()
        parentProcess = Process(target=self.computeFunc, args=(childCon, function,  iterator))
        parentProcess.start()
        res = parentCon.recv()
        parentProcess.join()
        return res
