from numpy import array_split
from pandas import DataFrame
from flockmp.utils.logger import FlockLogger
from inspect import isfunction
import dill


def split_chunks(objc, _type=None, size=100):
    # _type is not relevant anymore, how do I handle this case without breaking the interface?
    # for now I will only ignore the input and send a warning to the user

    if isinstance(objc, DataFrame):
        size = min(objc.shape[0], size)
        _it = array_split(objc, size)

    elif (isinstance(objc, list)):
        size = min(len(objc), size)
        _it = [objc[i::size] for i in range(size)]
    else:
        raise Exception("Not supported type")

    if _type:
        logger = FlockLogger()
        logger.warning("The argument _type is not necessary inside the function split_chunks anymore.")
    return _it


def isIter(value):
        try:
            _ = iter(value)
            return True
        except TypeError:
            return False


def isValidFunc(function):
    test1 = dill.pickles(function)
    test2 = isfunction(function)

    if all([test1, test2]):
        return True
    else:
        logger = FlockLogger()
        logger.error("Your function is not pickable")
        print("Function not pickable")
        return False
