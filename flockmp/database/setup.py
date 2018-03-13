#!/usr/bin/env python
from abc import ABCMeta, abstractproperty


class BaseDatabaseSetup(metaclass=ABCMeta):
    """
    :class:`BaseDatabaseSetup` used to enforce an interface to the user who desires to implement their own custom `DatabaseSetup`.

    """

    @abstractproperty
    def name(self):
        return None

    @abstractproperty
    def server(self):
        return None

    @abstractproperty
    def parameters(self):
        return None


class DatabaseSetup(object):
    """
    :class:`DatabaseSetup` used to build the connection that will be used inside your function in multiprocessing.

    """

    def __init__(self, name=None, server=None, parameters=None):
        self.name = name
        self.server = server
        self.parameters = parameters if parameters is not None else {}
