Multiprocessing your **Functions**
==================================

Flock supports the following list of functions:
    - Lambdas
    - Instance methods
    - Class methods
    - Regular functions

If your function needs a connection to any database to perform its computation, please use the :py:class:`~flockmp.database.DatabaseAsync` class.

.. autoclass:: flockmp.FunctionAsync
   :members: apply



Example
-------
.. code-block:: python
   :emphasize-lines: 2

   _list = list(range(2000))
   res = FunctionAsync.apply(_list, lambda x: x ** 2 / 10)
