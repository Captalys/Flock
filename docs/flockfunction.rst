Multiprocessing your **Functions**
==================================

It's supported the following list of functions:
    - Lambdas
    - Instance methods
    - Class methods
    - Regular functions

If you function needs connection to any database to perform its computation, please use the :py:class:`~flock.database.DatabaseAsync` class.

.. autoclass:: flock.FunctionAsync
   :members: apply



Example
-------
.. code-block:: python
   :emphasize-lines: 2

   _list = list(range(2000))
   res = FunctionAsync.apply(_list, lambda x: x ** 2 / 10)
