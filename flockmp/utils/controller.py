import psutil
from multiprocessing import Queue, Manager, Pipe
from flockmp.core import Executor
from time import sleep


class Controller(object):
    """
    Controller starts opening 1 executor
    """

    def __init__(self, watchTime=2, cpuPerc=70):
        self.watchTime = watchTime
        self._executors = []
        self.starting = True
        self.cpuPerc = self.cpuPerc

    def getSystemStats(self):
        """
        The idea of this method is to compute stats about the machine
        """

        # cpu metrics
        perc_cpu = np.mean(psutil.cpu_percent(interval=2, percpu=True))

        # memory metrics
        perc_mem = psutil.virtual_memory()[2]

        # disk metrics
        perc_disk = 10

        res = {}
        res["cpu"] = perc_cpu
        res["memory"] = perc_mem
        res["disk"] = perc_disk
        return res

    def spawnExecutor(self):
        NotImplementedError

    def hasImproved(self):
        """
        This method returns True if the performance improved or not
        """
        sleep(0.3)
        systemMetrics = self.getSystemStats()
        perc_cpu = systemMetrics.get("cpu")
        if perc_cpu <= self.cpuPerc:
            return True
        else:
            return False

    def cleaning(self):
        for ex in self._executors:
            ex.terminate()
        return


    def run(self, tasks, results, setups, progress, func):
        parentPipe, childPipe = Pipe()
        while True:
            if self.starting:
                print("Opening processes until the CPU hits 80% usage")
                ex = Executor(tasks, results, setups, childPipe, progress)
                ex.start()
                self._executors.append(ex)
                self.starting = False

                iterator = list(range(30000))
                for el in iterator:
                    tasks.put((func, (el, )))
                continue

            if (self.hasImproved() is True) and (len(results) <= len(iterator) * 0.8):
                ex = Executor(tasks, results, setups, childPipe, progress)
                ex.start()
                self._executors.append(ex)
                print("Num processos: ", len(self._executors))
                print("results", len(results))

            elif (len(results) == len(iterator)):
                break

        # killing all the executors there with poison pills
        for _ in range(len(self._executors)):
            tasks.put((None, None))

        # wait for all the results to end
        for _ in range(len(self._executors)):
            parentPipe.recv()

        # cleaning all executors yet left
        self.cleaning()
        print("all tasks done!")
        print("all killed")
        return


class TestingTasks(object):

    @staticmethod
    def test(value):
        import pandas as pd

        tmp = value ** 2
        df = pd.DataFrame({"a": 10 * [tmp], "b": 10 * [tmp]})
        sleep(0.1)
        return df

    def run(self):
        tasks = Queue()
        manager = Manager()
        results = manager.list()
        setups = None
        progress = None

        ct = Controller()
        ct.run(tasks, results, setups, progress, self.test)

        return


if __name__ == '__main__':
    tt = TestingTasks()
    tt.run()
