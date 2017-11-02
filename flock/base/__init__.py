import sys
from multiprocessing import Process, Pipe, Pool, Manager, Queue


class BaseMultiProc(object):
    """Documentation for BaseMultiProc

    """

    def __init__(self, poolSize=10, timeOutError=5):
        self.poolSize = poolSize
        self.timeOutError = timeOutError
        self.results = []
        self.queue = Queue()

    def getResults(self, result):
        self.results.append(result)

        
    def makeGlobal(self, dictGlobal):
        if dictGlobal is not None:
            for key in dictGlobal:
                globals()[key] = dictGlobal.get(key)

                
    def logErrors(self, localQueue):
        for asyncRes in localQueue:
            try:
                retQ = asyncRes.get(timeout=self.timeOutError)
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                

    def computeFunc(self, childCon, function, iterator, dictGlobal):
        pool = Pool(processes=self.poolSize, initializer=self.makeGlobal, initargs=(dictGlobal,))

        localQueue = []
        for it in iterator:
            asyncRes = pool.apply_async(function, args=(it,), callback=self.getResults)
            localQueue.append(asyncRes)
            
        pool.close()
        pool.join()
        
        self.logErrors(localQueue)
        childCon.send(self.results)


    def executeAsync(self, function, iterator, dictGlobal=None):
        parentCon, childCon = Pipe()
        parentProcess = Process(target=self.computeFunc, args=(childCon, function,  iterator, dictGlobal))
        parentProcess.start()
        res = parentCon.recv()
        parentProcess.join()
        return res



def f(a):
    try:
        b = (a ** 2) / global_constant
        return b
    except Exception as e:
        raise e
    
if __name__ == '__main__':

    iterator = list(range(10))
    dictGlobal = {"global_constant": 10}
    bp = BaseMultiProc()
    res = bp.executeAsync(f, iterator, dictGlobal)
    print(res)
