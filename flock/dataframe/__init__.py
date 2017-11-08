from flock.base import BaseMultiProc
from flock.tools import split_chunks
from pandas import concat


class DataFrameAsync(object):
    """
    DOC STRING DA CLASSE
    """

    @classmethod
    def applyInRows(cls, args):
        """
        :func:`Applyinrows` method takes a dataframe and the function to be applied at as arguments. Stores every row of the dataframe at a list.
        Through :func:`executeAsync()`   BaseMultiProc's method, it processes the fuctions at each element of the list (row) in parallel calling different processes and 
        in the end returns the resulting Dataframe by concating the processed rows.  

        func: Function that will be applied at the Dataframe 

        df: Dataframe passed as argument

        """
        func, block_df = args
        _df2 = block_df.copy()
        list_rows = []

       
        for i in range(len(_df2)):
            list_rows.append(_df2.iloc[i:i+1])

        bp2 = BaseMultiProc()
        
        res2 = bp2.executeAsync(func, list_rows)
        res2 = concat(res2)
        return res2


    @classmethod
    def apply(cls, dataframe, function, style="row-like",
              chunksize=100, poolSize=5):
        """
        Apply method receives the dataframe,  the function you want to apply on it, style, chunksize and poolsize.  The first step is the segmentation of the orgininal dataframe in chunks, generating a list of 
        dataframes called iterator. Then the :func:`executeAsync()` will parallelize the function's operatations on the segmented dataframes and then concatenate the chunks, returning the 
        excepted result. There two options for the way it will operate, as 'row-like' or 'block-like'

        dataframe: Input Dataframe

        fuction: Function  to be applied on the dataframe

        chunksize: Defines on how many chunks will the original dataframe be splitted 

        poolSise: Defines number of  pools of processes

        style: if  set as "row-like", the list of dataframes resulted from the chunking process is passed along with 
        the function to the 'Applyinrows' to the :func:`executeAsync()`. Basically what will happen is that the process on :func:`Applyinrows` will occur for a list of dataframes, in parellel. While, if it is passed as "Block-like",  the 
        the process is similar to the method :func:`Applyinrows` but will happen for the whole list of dataframes.
        


        """
        _df = dataframe.copy()
        #lista de dfs
        iterator = split_chunks(_df, _type="dataframe", size=chunksize)

        bp = BaseMultiProc(poolSize=poolSize)

        #if row-like, 
        if style == "row-like":
            iterator = [(function, el) for el in iterator]
            res = bp.executeAsync(cls.applyInRows, iterator)

        elif style == "block-like":
            res = bp.executeAsync(function, iterator)

        else:
            raise Exception("Style-type not supported")

        res = concat(res)
        res = res.sort_index()
        return res
        """
        TESTE
        """


if __name__ == '__main__':
    dt = DataFrameAsync()
  