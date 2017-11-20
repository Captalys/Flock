from numpy import array_split
from flockmp.utils.logger import FlockLogger
import dill


def split_chunks(objc, _type, size=100):

    if _type == "dataframe":
        size = min(objc.shape[0], size)
        _it = array_split(objc, size)
    elif _type == "list":
        size = min(len(objc), size)
        _it = [objc[i::size] for i in range(size)]
    else:
        raise Exception("Not supported type")
    return _it


def isIter(value):
        try:
            _ = iter(value)
            return True
        except TypeError:
            return False


def isValidFunc(function):
    res = dill.pickles(function)
    if res:
        return True
    else:
        logger = FlockLogger()
        logger.error("Your function is not pickable")
        print("Function not pickable")
        return False
