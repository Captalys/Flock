import pytest
import pandas as pd
from flockmp.utils import isIter, isValidFunc, split_chunks


class TestUtils(object):

    @staticmethod
    def validFunction(value):
        value += 1
        return value

    def test_iter(self):
        assert isIter(range(10)) == True
        assert isIter("Testing strings") == True
        assert isIter(list(range(10))) == True
        assert isIter(10) == False
        assert isIter(isIter) == False

    def test_valid_function(self):
        validF1 = lambda x: x ** 2
        assert isValidFunc(validF1) == True
        assert isValidFunc(self.validFunction) == True
        assert isValidFunc(isIter) == True
        assert isValidFunc(isIter(10)) == False


    def test_dataframe_split(self):
        df = pd.DataFrame({"col1": list(range(1000)), "col2": list(range(1000, 2000))})

        size = 10
        list_split = split_chunks(df, size=size)
        assert len(list_split) == size

        size = 3000
        list_split = split_chunks(df, size=size)
        assert len(list_split) == min([len(list_split), size])

        with pytest.raises(Exception):
            array = np.array(list(range(20)))
            list_split = split_chunks(array, "list", size=size)
