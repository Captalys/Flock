from multiprocessing import Process, Queue, JoinableQueue, Pipe
import sys
from time import sleep


class Executor(Process):

    def __init__(self, taskQueue, resultQueue, databaseSetup, childPipe):
        super(Executor, self).__init__()
        self.taskQueue = taskQueue
        self.resultQueue = resultQueue
        self.databaseSetup = databaseSetup
        self.childPipe = childPipe

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
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

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

    def apply(self, function, iterator):

        tasks = JoinableQueue()
        results = Queue()

        listExSize = min(self.numProcesses, len(iterator))
        parentPipe, childPipe = Pipe()

        executors = [Executor(tasks, results, self.setups, childPipe) for _ in range(listExSize)]

        for ex in executors:
            ex.start()

        # make the inputs iterator
        inputs = []
        for parameter in iterator:
            if not self.isIter(parameter):
                parameter = (parameter, )
            inputs.append((function, parameter))

        for _inpt in inputs:
            tasks.put(_inpt)

        poisonPills = [(None, None)] * listExSize
        for pill in poisonPills:
            tasks.put(pill)

        tasks.join()

        for _ in range(listExSize):
            parentPipe.recv()

        # get all the results:
        res = []

        while not results.empty():
            _r = results.get()
            res.append(_r)
        return res
