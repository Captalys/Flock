import psutil


class Controller(object):

    def getSystemStats(self):
        """
        The idea of this method is to compute stats about the machine
        """
        return psutil.cpu_percent()

    def spawnExecutor(self):
        NotImplementedError

    def hasImproved(self):
        """
        This method returns True if the performance improved or not
        """
        pass



if __name__ == '__main__':
    ct = Controller()
    ret = ct.getSystemStats()
    print(ret)
