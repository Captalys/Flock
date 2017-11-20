from flockmp.list import ListAsync
import unittest


class TestList(unittest.TestCase):

    def funcHelper1(self, x):
        b = x ** 2
        return b

    def testList(self):
        size = 2000
        _list = list(range(size))
        res = ListAsync.apply(_list, self.funcHelper1)
        self.assertEqual(len(res), size)

    def testListLambda(self):
        size = 1000
        _list = list(range(size))
        res = ListAsync.apply(_list, lambda x: x / 2)
        self.assertEqual(len(res), size)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
