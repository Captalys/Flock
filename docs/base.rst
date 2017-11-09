Flock Base class
================

.. autoclass:: flock.base.BaseMultiProc
   :members: executeAsync


Example
-------
.. code-block:: python
   :emphasize-lines: 3

   bp = BaseMultiProc()
   iterator = list(range(10))
   res = bp.executeAsync(lambda x: x ** 2, iterator)
