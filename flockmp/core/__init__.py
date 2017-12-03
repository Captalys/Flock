import sys
from time import sleep
from multiprocessing import Process
from flockmp.utils.logger import FlockLogger


class Executor(Process):

    def __init__(self, taskQueue, resultManager, databaseSetup, childPipe, progress):
        super(Executor, self).__init__()
        self.taskQueue = taskQueue
        self.resultManager = resultManager
        self.progressQueue = progress
        self.databaseSetup = databaseSetup
        self.childPipe = childPipe
        self.SENTINEL = 1

    def sendData(self, res):
        while True:
            try:
                self.resultManager.append(res)
                break
            except ConnectionRefusedError as err:
                sleep(0.3)  # no tight loops
                continue
        return

    def run(self):
        # setting up the environment
        kwargs = {}

        try:
            if self.databaseSetup is not None:

                if not isinstance(self.databaseSetup, list):
                    self.databaseSetup = [self.databaseSetup]

                for inst in self.databaseSetup:
                    dbPar = inst.parameters
                    parName = inst.name
                    con = inst.server(**dbPar)
                    if parName is not None:
                        kwargs[parName] = con

            flag = True
            while True:
                try:
                    _function, args = self.taskQueue.get()

                    if _function is None:
                        flag = False
                        break
                    else:
                        res = _function(*args, **kwargs)

                    self.sendData(res)
                except Exception as e:
                    logger = FlockLogger()
                    logger.error("Function failed! Line {} {} {}".format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))
                finally:
                    if (self.progressQueue is not None) and (flag is True):
                        self.progressQueue.put(self.SENTINEL)
        except Exception as e:
            logger = FlockLogger()
            logger.error("Worker failed! - {} - {}".format(type(e).__name__, e))

        self.childPipe.send('Job done!')
        return True
