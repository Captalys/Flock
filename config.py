import configparser
from importlib import import_module
import os


def readConfig():
    cfg = configparser.ConfigParser()

    if os.path.isfile('config.ini'):
        cfg.read('config.ini')
        return cfg
    else:
        raise Exception("config.ini file was not found")


def getDatabases():
    cfg = readConfig()
    kwargs = {}

    if 'database' not in cfg:
        print("There are no database config in your config.ini")
        return kwargs

    cfg = cfg["database"]
    for key in cfg:
        try:
            _mod, _cls, _fun = cfg.get(key).rsplit(".", 2)
            _module = import_module(_mod)
            _class = getattr(_module, _cls)
            _func = getattr(_class, _fun)
            kwargs[key] = _func
        except ImportError as err:
            print("Flock Error: ", err)
    return kwargs


if __name__ == '__main__':
    res = getDatabases()
    print(res)
