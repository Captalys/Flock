from flockmp.database import DatabaseAsync
from flockmp.utils.errors import FunctionNotPickled
import pytest


class TestDatabaseAsync(object):


    @staticmethod
    def myFunction(value):
        tmp = value ** 2
        return tmp

    def notPickableFunction(self, value):
        tmp = value ** 2
        return tmp

    def test_basic(self):
        db = DatabaseAsync(checkProgress=False, numProcesses=200)
        iterator = 10000 * [1, 2, 3, 4, 5, 6]
        res = db.apply(self.myFunction, iterator)
        assert len(res) == 60000

    def test_not_pickled(self):
        db = DatabaseAsync(checkProgress=False, numProcesses=100)
        iterator = 10 * [1, 2, 3, 4]
        with pytest.raises(FunctionNotPickled):
            res = db.apply(self.notPickableFunction, iterator)

    def test_num_process(self):
        _num = 1000
        db = DatabaseAsync(checkProgress=False, numProcesses=_num)
        iterator = 10 * [1, 2, 3]

        # number of processes is way to large. Flock tends to use the minimum between numProcess and iterator size
        res = db.apply(self.myFunction, iterator)
        assert db._outputSize == len(iterator)
