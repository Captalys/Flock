from flockmp.list import ListAsync


class TestList(object):

    def funcHelper1(self, x):
        b = x ** 2
        return b

    def testList(self):
        size = 2000
        _list = list(range(size))
        res = ListAsync.apply(_list, self.funcHelper1)
        assert len(res) == size

    def testListLambda(self):
        size = 1000
        _list = list(range(size))
        res = ListAsync.apply(_list, lambda x: x / 2)
        assert len(res) == size
