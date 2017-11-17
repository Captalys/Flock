from multiprocessing import Process, Queue, JoinableQueue, Pipe
import sys
import os
import dill
from tqdm import tqdm
from time import sleep
from flock.utils.logger import FlockLogger


class Executor(Process):

    def __init__(self, taskQueue, resultQueue, databaseSetup, childPipe, progress):
        super(Executor, self).__init__()
        self.taskQueue = taskQueue
        self.resultQueue = resultQueue
        self.progressQueue = progress
        self.databaseSetup = databaseSetup
        self.childPipe = childPipe
        self.SENTINEL = 1

    def run(self):
        # setting up the environment
        kwargs = {}
        if self.databaseSetup is not None:

            if not isinstance(self.databaseSetup, list):
                self.databaseSetup = [self.databaseSetup]

            for inst in self.databaseSetup:
                dbPar = inst.parameters
                parName = inst.name
                con = inst.server(**dbPar)
                if parName is not None:
                    kwargs[parName] = con

        while True:
            try:
                _function, args = self.taskQueue.get()

                if _function is None:
                    self.taskQueue.task_done()
                    break
                else:
                    res = _function(*args, **kwargs)

                self.taskQueue.task_done()
                self.resultQueue.put(res)
                self.progressQueue.put(self.SENTINEL)
            except Exception as e:
                self.taskQueue.task_done()
                logger = FlockLogger()
                logger.error("line {} {} {}".format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))

        self.childPipe.send('Job done!')
        return True


class DatabaseAsync(object):

    def __init__(self, setups=None, numProcesses=5):
        self.numProcesses = numProcesses
        self.setups = setups

    def isIter(self, value):
        try:
            _ = iter(value)
            return True
        except TypeError:
            return False

    def progressBar(self, queueProgress, queueSize):
        pbar = tqdm(total=queueSize)
        for _ in iter(queueProgress.get, None):
            pbar.update()
        pbar.close()

    def clear(self):
        os.system('cls' if os.name == "nt" else "clear")

    def valid(self, function):
        res = dill.pickles(function)
        if res:
            return True
        else:
            logger = FlockLogger()
            logger.error("Your function is not pickable")
            return False

    def apply(self, func, iterator):
        logger = FlockLogger()

        if not self.valid(func):
            print("There is an error with your function. Look at the logging files.")
            return

        tasks = JoinableQueue()
        results = Queue()
        progress = Queue()

        listExSize = min(self.numProcesses, len(iterator))
        parentPipe, childPipe = Pipe()

        self.clear()
        print("Progress of execution tasks...")
        prgBar = Process(target=self.progressBar, args=(progress, len(iterator)))
        prgBar.start()

        executors = [Executor(tasks, results, self.setups, childPipe, progress) for _ in range(listExSize)]

        for ex in executors:
            ex.start()

        # make the inputs iterator
        inputs = []
        for parameter in iterator:
            if not self.isIter(parameter):
                parameter = (parameter, )
            inputs.append((func, parameter))

        for _inpt in inputs:
            tasks.put(_inpt)

        poisonPills = [(None, None)] * listExSize
        for pill in poisonPills:
            tasks.put(pill)

        tasks.join()

        # wait for all the results to end
        for _ in range(listExSize):
            parentPipe.recv()

        # finish progress bar queue
        progress.put(None)

        # get all the results:
        res = []

        sleep(0.01)  # really, too fast in the main queue
        print("Fetching all the results...")
        pbarLocal = tqdm(total=len(iterator))
        while not results.empty():
            _r = results.get()
            res.append(_r)
            pbarLocal.update()
        pbarLocal.close()
        logger.info("Successful processing of the function {}".format(func.__name__))
        return res


def teste(val):
    return val ** 2


if __name__ == '__main__':
    db = DatabaseAsync()
    iterator = 1 * [1, 2, 3, 4, 5, 6]
    res = db.apply(teste, iterator)
