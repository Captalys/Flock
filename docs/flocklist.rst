Multiprocessing **List** objects
================================

.. autoclass:: flock.list.ListAsync
   :members: apply


Example
-------
.. code-block:: python
   :emphasize-lines: 2

   _list = list(range(2000))
   res = ListAsync.apply(_list, lambda x: x ** 2 / 10)
