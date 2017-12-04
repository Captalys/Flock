from multiprocessing import Process, Queue, JoinableQueue, Pipe, Manager
import sys
import os
import dill
from tqdm import tqdm
from time import sleep
from flockmp.utils.logger import FlockLogger
from flockmp.utils.errors import FunctionNotPickled
from flockmp.utils import isIter, isValidFunc
from flockmp.core import Executor


class DatabaseAsync(object):

    def __init__(self, setups=None, numProcesses=5, checkProgress=True):
        self.numProcesses = numProcesses
        self.setups = setups
        self.checkProgress = checkProgress
        self._numUsedProcess = None
        self._outputSize = None
        self._anyErrors = False

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

    def checkLength(self, managerList, iterLength):
        while True:
            try:
                if len(managerList) == iterLength:
                    return True
                else:
                    return False
            except ConnectionRefusedError as err:
                continue

    def apply(self, func, iterator):
        logger = FlockLogger()

        if not isValidFunc(func):
            self._anyErrors = True
            raise FunctionNotPickled

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

        if not self.checkLength(results, len(iterator)):
            self._anyErrors = True
            logger.error("The return list object does not have the same size as your input iterator.")

        # headshot remaining zombies
        for ex in executors:
            ex.terminate()

        # logging some info after running the apply
        self._outputSize = len(results)
        self._numUsedProcess = listExSize

        return results
