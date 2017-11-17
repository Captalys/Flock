import os
import errno
import gitpath
import logging
from datetime import datetime


class FlockLogger(logging.getLoggerClass()):

    def __init__(self, logType='informative', folderName='logs', ext="txt"):
        super(FlockLogger, self).__init__(name=__name__)
        self.folderName = folderName
        self.extension = ext
        self.logType = logType
        self.setup()

    def getFileName(self):
        now = datetime.now()
        year, month, day = str(now.year), str(now.month), str(now.day)
        fpath = gitpath.root() + "/" + self.folderName + "/" + year
        fpath = fpath + "/" + month + "/" + day + "/" + self.logType + "." + self.extension
        return fpath

    def createFile(self, fileName):
        if not os.path.exists(os.path.dirname(fileName)):
            try:
                os.makedirs(os.path.dirname(fileName))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with open(fileName, "a+") as f:
            if os.stat(fileName).st_size == 0:
                f.write("Welcome to the beginning of the {} FlockLogger!!\n".format(self.logType.title()))
                f.write("Flock is a Captalys Data Science Project.\n\n\n")
            else:
                f.write("")
        return True

    def setup(self):
        fileName = self.getFileName()
        self.createFile(fileName)
        fhandler = logging.FileHandler(fileName)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        fhandler.setFormatter(formatter)
        self.addHandler(fhandler)
        self.setLevel(logging.INFO)
        return True


if __name__ == '__main__':
    fl = FlockLogger("informative")
    fl.info("Testing all this little things")
    fl.warning("Hey Jude, take a look at this use case. It might become deprecated")
    fl.error("I told you so... not working anymore")
