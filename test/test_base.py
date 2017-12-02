from flockmp.base import BaseMultiProc
import pytest


class TestBase(object):

    def funcHelper1(self, a):
        try:
            b = (a ** 2)
            return b
        except Exception as e:
            raise e

    def testExecuteAsync(self):
        bp = BaseMultiProc()
        iterator = list(range(10))
        res = bp.executeAsync(self.funcHelper1, iterator)
        assert len(res) == 10
        assert max(res) == 81
