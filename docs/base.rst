Flock Base class
================

Base class used to build the :py:class:`~flockmp.list.ListAsync`, :py:class:`~flockmp.dataframe.DataFrameAsync` and :py:class:`~flockmp.FunctionAsync` classes.

You should avoid using this class inside your code. The interface might change without previous notice.


.. autoclass:: flockmp.base.BaseMultiProc
   :members: executeAsync


Example
-------
.. code-block:: python
   :emphasize-lines: 3

   bp = BaseMultiProc()
   iterator = list(range(10))
   res = bp.executeAsync(lambda x: x ** 2, iterator)
