Getting Started
===============


    - Go to the :doc:`setup` page.
    - Learn the basic concepts of Flock.
      	- :py:class:`~flockmp.FunctionAsync`
	- :py:class:`~flockmp.dataframe.DataFrameAsync`
	- :py:class:`~flockmp.list.ListAsync`
	- :py:class:`~flockmp.database.DatabaseAsync`
	    
    - Dive in to other tutorials below.
        - `Basic Function`_
	- `Lambdas`_
	- `Instance methods`_
	- `DataFrames`_
	- `Database dependent functions`_
	    
	  

Basic Function
--------------
      We only need to define our iterator, which are the elements that will be applied to the given function. After that, we use the :func:`apply` from the :py:class:`~flockmp.FunctionAsync`.

.. code-block:: python
   :emphasize-lines: 6
		     
      def myFunction(value):
          tmp = value ** 2
          return tmp
	   
      iterator = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      res = FunctionAsync.apply(iterator, myFunction)
      res>
           [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]


Lambdas
-------

    Usage is the same if you have a :func:`lambda` function.
    
.. code-block:: python
   :emphasize-lines: 2
	   
      iterator = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      res = FunctionAsync.apply(iterator, lambda x: x ** 2)
      res>
           [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]



Instance methods
----------------

    The regular :mod:`multiprocessing` module can't handle instance methods very well because they are not `picklable` objects. However, you can continue to use the same interface as before for instance methods.

.. code-block:: python
   :emphasize-lines: 10

      class Test(object):
          def compute(self, foo, bar):
	      tmp = foo + bar
	      res = tmp ** foo
	      return res


      inst = Test()
      iterator = [(val1, val2) for val1, val2 in zip([1,2,3,4], [10,20,30,40])]
      res = FunctionAsync(iterator, inst.compute)
      res>
           [11, 44, 99, 176]



DataFrames
----------

   There are two use cases related to DataFrames already implemented. First, you might want to execute the :func:`apply` function in a row-by-row basis. For example, in order to create a new column using two existent columns.
   
.. code-block:: python

   df = DataFrame({"foo": [5, 10, 15, 20],
		   "bar": [1, 2, 3, 4]})
   df["new-var"] = DataFrameAsync.apply(df[["foo", "bar"]],
                                       lambda x: (x["foo"] + x["bar"]) ** 2, style="row-like")

Using the previous method, :mod:`Flock` will split your DataFrame into chunks, send each chunk to a specific process, and inside each process it will multiprocess each row. This approach is very scalable if you have a very large dataframe and only want to perform an apply method.


The next use case is block based. Imagine you want to use your entire dataframe as input to some operation that will be applied to every column.

.. code-block:: python

   df = DataFrame({"foo": list(range(1000)),
		   "bar": list(range(2000, 3000))})
   df_new = DataFrameAsync.apply(df, lambda x: x ** 2, style="block-like")

   
		   
Database dependent functions
----------------------------

   This is a very useful class if you work with many databases in your code base. One of the main problems with multiprocessing and databases is related to the impossibility of sending a `connection` object to each open process. This becomes very annoying since you have multiple databases with several drivers.

   One known solution to this problem is the guidance to open your connection inside the multiprocessed function. However, this is a very bad idea sometimes because the time you might take to connect can be very long and you will not gain the full benefits of multiprocessing.

   The strategy adopted by :mod:`Flock` is to divide this problem into two steps. First, you need to create a :py:class:`~flock.database.setup.DatabaseSetup` instance to inform all the connections and name variables you are using inside the function you desire to multiprocess.

   Using this instance, :mod:`Flock` will establish all your needed connections only once per process and reuse the connections for each task that processes get assigned to perform. Let's see that in action mocking a MySQL connection (SQLAlchemy) and a Apache Cassandra connection (cassandra-driver).


.. code-block:: python

   def myFunction(value, cass_con, mysql_con):
       getData = pd.read_sql("select * from cool_table", mysql_con)
       saveData = cass_con.execute("insert data to your cassandra_cool table")
       return True
   

   # you probably have a method to connect to the database. Send the method without making the call
   mysqlCreateCon = MysqlConnectionClass.yourConnectMethod
   cassCreateCon = CassandraConnectionClass.yourConnectMethod


   # create the setup instances
   mysqlSetup = DatabaseSetup(server=mysqlCreateCon, name="mysql_con",
		              parameters={"password": "password1", "user": "root"})
			      
   cassSetup = DatabaseSetup(server=cassCreateCon, name="cass_con",
		              parameters={"keyspace": "__default__", "ip": "0.0.0.0"})

  # now we send the two setup connections to the databaseasync
  dbAsync = DatabaseAsync(setups=[mysqlSetup, cassSetup])
  res = dbAsync.apply(iterator=[1, 2, 3, 4, 5, 6], myFunction)
   
   

In the setup process, the attribute `name` should be the same value as the `variable name` inside the :func:`myFunction` that will be processed.
As you can see, the setup process can be a little boring, so we have a :py:class:`~flockmp.database.setup.BaseDatabaseSetup` to be extended and you can hide all this portion inside your code.
