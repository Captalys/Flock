from multiprocessing import Process, Queue, JoinableQueue
from weddell.database.sql import SqlCon


class Executor(Process):

    def __init__(self, taskQueue, resultQueue, dictCon=None):
        super(Executor, self).__init__()
        self.taskQueue = taskQueue
        self.resultQueue = resultQueue
        self.dictCon = dictCon

    def getConnection(self, connectionName):
        if connectionName is None:
            func = None
        else:
            conns = {"sql": SqlCon.sql_connection,
                     "mysql": SqlCon.mysql_connection}
            func = conns.get(connectionName, None)
        return func

    def run(self):
        # setting up the environment
        kwargs = {}
        if self.dictCon is not None:
            for key in self.dictCon:
                con = self.getConnection(self.dictCon.get(key, None))()
                kwargs[key] = con

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

    def __init__(self, numProcesses=5):
        self.numProcesses = numProcesses

    def apply(self, function, iterator, dictCon=None):

        tasks = JoinableQueue()
        results = Queue()

        listExSize = min(self.numProcesses, len(iterator))

        executors = [Executor(tasks, results, dictCon) for _ in range(listExSize)]

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


class Inst(object):

    def run(self, val):
        return "CHEGUEI INSTANCIADO RAPA"


if __name__ == '__main__':
    dbAsync = DatabaseAsync()
    # dictCon = {"sql": {"varName": "sql_con", "parameters": ["schema"]},
    #            "mysql": {"varName": "mysql_con", "parameters": ["schema", "table"]}}
    dictCon = {"sql_con": "sql",
               "mysql_con": "mysql"}
    inputs = [(el,) for el in range(10)]
    res = dbAsync.apply(Inst().run, inputs)
    print(res)
