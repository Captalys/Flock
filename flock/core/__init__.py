from flock.base import BaseMultiProc
from flock.tools import split_chunks
from pandas import DataFrame, concat

def applyAsync(objc, func, poolSize=10):
    """
    objc:  should contain only the values that will be used by the func
    return:
    List of values returned from the func
    """
    if isinstance(objc, DataFrame):
        _df = objc.copy()
        iterator = split_chunks(_df, _type="dataframe")
    elif isinstance(objc, list):
        iterator = objc
    else:
        raise Exception("Not supported type")
        
    bp = BaseMultiProc(poolSize=poolSize)
    res = bp.executeAsync(func, iterator)
    # format the returned values
    if isinstance(objc, DataFrame):
        res = concat(res)
    
    return res
