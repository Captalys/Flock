from multiprocessing import Process, Queue, JoinableQueue
from abc import ABCMeta, abstractproperty


class Executor(Process):

    def __init__(self, taskQueue, resultQueue, databaseSetup):
        super(Executor, self).__init__()
        self.taskQueue = taskQueue
        self.resultQueue = resultQueue
        self.databaseSetup = databaseSetup

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
                kwargs[parName] = con

            print("Alive", con)

        while True:
            function, args = self.taskQueue.get()

            if function is None:
                self.taskQueue.task_done()
                break
            else:
                res = function(*args, **kwargs)

            self.taskQueue.task_done()
            self.resultQueue.put(res)
        return True


class DatabaseAsync(object):

    def __init__(self, setups=None, numProcesses=5):
        self.numProcesses = numProcesses
        self.setups = setups

    def apply(self, function, iterator):

        tasks = JoinableQueue()
        results = Queue()

        listExSize = min(self.numProcesses, len(iterator))

        executors = [Executor(tasks, results, self.setups) for _ in range(listExSize)]

        for ex in executors:
            ex.start()

        # make the inputs iterator
        inputs = [(function, el) for el in iterator]
        for _inpt in inputs:
            tasks.put(_inpt)

        poisonPills = [(None, None)] * listExSize
        for pill in poisonPills:
            tasks.put(pill)

        tasks.join()

        # get all the results:
        res = []
        while not results.empty():
            _r = results.get()
            res.append(_r)
        return res


class BaseDatabaseSetup(metaclass=ABCMeta):

    @abstractproperty
    def name(self):
        return None

    @abstractproperty
    def server(self):
        return None

    @abstractproperty
    def parameters(self):
        return None


class DatabaseSetup(object):

    def __init__(self, name, server, parameters):
        self.name = name
        self.server = server
        self.parameters = parameters
