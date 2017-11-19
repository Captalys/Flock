Flock Base class
================

Base class used to build the :py:class:`~flock.list.ListAsync`, :py:class:`~flock.dataframe.DataFrameAsync` and :py:class:`~flock.FunctionAsync` classes.

You should avoid using this class inside your code. The interface might change without previous notice.


.. autoclass:: flock.base.BaseMultiProc
   :members: executeAsync


Example
-------
.. code-block:: python
   :emphasize-lines: 3

   bp = BaseMultiProc()
   iterator = list(range(10))
   res = bp.executeAsync(lambda x: x ** 2, iterator)
