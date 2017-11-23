Multiprocessing **DataFrame** objects
=====================================

.. autoclass:: flockmp.dataframe.DataFrameAsync
   :members: apply

Example
-------
.. code-block:: python
   :emphasize-lines: 3

   df = DataFrame({"a": list(range(1000)),
		   "b": list(range(1000, 2000))})
   res = DataFrameAsync.apply(df, lambda x: x ** 2, style="block-like")
