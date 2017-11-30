from multiprocessing import Process, Queue, JoinableQueue, Pipe, Manager
import sys
import os
import dill
from tqdm import tqdm
from time import sleep
from flockmp.utils.logger import FlockLogger
from flockmp.utils import isIter, isValidFunc


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
                sleep(0.2)  # no tight loops
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


class DatabaseAsync(object):

    def __init__(self, setups=None, numProcesses=5, checkProgress=True):
        self.numProcesses = numProcesses
        self.setups = setups
        self.checkProgress = checkProgress

    def progressBar(self, queueProgress, queueSize):
        pbar = tqdm(total=queueSize)
        for _ in iter(queueProgress.get, None):
            if _ is not None:
                pbar.update()
        pbar.close()

    def getProgressBar(self, sizeIter):
        if self.checkProgress:
            progress = Queue()
            self.clear()
            print("Progress of execution tasks...")
            prgBar = Process(target=self.progressBar, args=(progress, sizeIter))
            prgBar.start()
        else:
            progress = None
        return progress

    def sendInputs(self, tasks, func, iterator):
        for parameter in iterator:
            if not isIter(parameter):
                parameter = (parameter, )
            tasks.put((func, parameter))
        return

    def clear(self):
        os.system('cls' if os.name == "nt" else "clear")

    def apply(self, func, iterator):
        logger = FlockLogger()

        if not isValidFunc(func):
            print("There is an error with your function. Look at the logging files.")
            return

        tasks = Queue()

        manager = Manager()
        results = manager.list()

        listExSize = min(self.numProcesses, len(iterator))
        parentPipe, childPipe = Pipe()

        progress = self.getProgressBar(sizeIter=len(iterator))
        executors = [Executor(tasks, results, self.setups, childPipe, progress) for _ in range(listExSize)]

        for ex in executors:
            ex.start()

        self.sendInputs(tasks, func, iterator)

        # kill each executor processes
        poisonPills = [(None, None)] * listExSize
        for pill in poisonPills:
            tasks.put(pill)

        # wait for all the results to end
        for _ in range(listExSize):
            parentPipe.recv()

        if self.checkProgress:
            # finish progress bar queue
            progress.put(None)

        if len(results) != len(iterator):
            logger.error("The return list object does not have the same size as your input iterator.")

        # headshot remaining zombies
        for ex in executors:
            ex.terminate()

        return results


def teste(val):
    return val ** 2


if __name__ == '__main__':
    db = DatabaseAsync(checkProgress=True, numProcesses=200)
    iterator = 10000 * [1, 2, 3, 4, 5, 6]
    res = db.apply(teste, iterator)
    print("final", len(res))
