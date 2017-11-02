from numpy import array_split

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
