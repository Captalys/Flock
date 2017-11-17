import os
import errno
import logging
from datetime import datetime
from pathlib import Path


class FlockLogger(object):

    def __init__(self, folderPath='default', ext="txt"):
        self.folderPath = folderPath
        self.extension = ext
        self.__hasInfo = None
        self.__hasWarning = None
        self.__hasError = None

    def getFileName(self, logType):
        if self.folderPath == "default":
            fpath = str(Path.home())
        else:
            fpath = self.folderPath
        now = datetime.now()
        year, month, day = str(now.year), str(now.month), str(now.day)
        fpath = fpath + "/" + ".flock" + "/" + year
        fpath = fpath + "/" + month + "/" + day + "/" + logType + "." + self.extension
        return fpath

    def createFile(self, fileName, logType):
        if not os.path.exists(os.path.dirname(fileName)):
            try:
                os.makedirs(os.path.dirname(fileName))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with open(fileName, "a+") as f:
            if os.stat(fileName).st_size == 0:
                f.write("Welcome to the beginning of the {} FlockLogger!!\n".format(logType.title()))
                f.write("Flock is a Captalys Data Science Project.\n\n\n")
            else:
                f.write("")
        return True

    def setup(self, logType):
        fileName = self.getFileName(logType)
        self.createFile(fileName, logType)
        logger = logging.getLogger(logType)
        fhandler = logging.FileHandler(fileName)
        formatter = logging.Formatter("%(asctime)s %(levelname)s SourceFile: %(pathname)s ProcessName: %(processName)s Line: %(lineno)d Message: %(message)s")
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        logger.setLevel(logging.INFO)
        return logger

    def info(self, message):
        if not self.__hasInfo:
            logger = self.setup(logType='informative')
            self.loggerInfo = logger
        self.loggerInfo.info(message)
        return

    def warning(self, message):
        if not self.__hasWarning:
            logger = self.setup(logType='warnings')
            self.loggerWarning = logger
        self.loggerWarning.warning(message)
        return

    def error(self, message):
        if not self.__hasError:
            logger = self.setup(logType='errors')
            self.loggerError = logger
        self.loggerError.error(message)
        return


if __name__ == '__main__':
    fl = FlockLogger()
    fl.info("Testing all this little things")
    fl.warning("Hey Jude, take a look at this use case. It might become deprecated")
    fl.error("I told you so... not working anymore")
