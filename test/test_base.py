from flock.base import BaseMultiProc
import unittest



class TestBase(unittest.TestCase):

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
        self.assertEqual(len(res), 10)
        self.assertEqual(max(res), 81)
        


def main():
    unittest.main()


    
if __name__ == '__main__':
    main()
