# Flock Multiprocessing

[![buddy pipeline](https://104.154.213.146:17003/captalys/flock/pipelines/pipeline/1/badge.svg?token=66ad3d889d3b182491f0ca4715770f5e870e7e2f590d98ee60bcac0da9d9d623 "buddy pipeline")](https://104.154.213.146:17003/captalys/flock/pipelines/pipeline/1)

Python library for Duck-like multiprocessing 

Flock is intended to help you to easily apply multiprocessing in your development code without thinking too much.

The system is capable of easily setup a multiprocessing environment to handle instance methods, class methods, lambdas and regular functions to be applied to any iterable. See the documentation [Getting Started!](http://flock.readthedocs.io/en/master/starting.html)


When the function to be multiprocessed makes any interaction with **databases** we run into trouble because connections are not allowed to be passed through processes inside messages. In order to handle this situation, we developed the **DatabaseAsync** class, [check it out](http://flock.readthedocs.io/en/master/starting.html#database-dependent-functions)


One advantage for using this library is to build one more layer of abstraction in multiprocessing tasks. You don't need to think too much about how to manage the right settings to accomplish your task. "I want to apply multiprocessing in this list! Ok. `FunctionAsync.apply(list, function)`, done."


# Examples

### 1. Apply a function in every element of the iterator

The example below works for ~lambdas~, ~instance methods~ and ~class methods~ too.

``` python
from flockmp import FunctionAsync

def myFunction(value):
    tmp = value ** 2
    return tmp

iterator = list(range(10))
res = FunctionAsync.apply(iterator, myFunction)
res > [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### 2. Apply a function that has dependencies with a database

If you work with many databases in your code you should be using this functionality because Python does not allow you to transmit database connections to multiprocessing Processes.


``` python

from flockmp.database import DatabaseAsync
from flockmp.database.setup import DatabaseSetup
import pandas as pd


def myFunction(value, cassandra_con, mysql_con):
    getData = pd.read_sql("select * from cool_table", mysql_con)
    saveData = cassandra_con.execute("insert data into your cassandra_cool table")
    return

# create the one setup instance for the Cassandra connection and another for Mysql
mysqlSetup = DatabaseSetup(server=mysqlCreateCon, variable_name="mysql_con",
                           parameters={"password": "123",
                                       "user": "root"})

cassandraSetup = DatabaseSetup(server=cassandraCreateCon, variable_name="cassandra_con",
                               parameters={"password": "123",
                                           "user": "root"})

# the server parameter is some method that you used to use to connect into these databases
# the variable_name is the name of the database variable inside your function

# now we send the two setup connections to the databaseasync
dbAsync = DatabaseAsync(setups=[mysqlSetup, cassSetup])

# apply the function to the iterator
res = dbAsync.apply(iterator=[1, 2, 3, 4, 5, 6], myFunction)
```

You see that `DatabaseSetup`s are not so cool to perform every time from scratch, therefore we have a `DatabaseSetupBase` that you can inherited and create your own version of `DatabaseSetup` to be used anywhere in your code.



### 3. Apply function to DataFrame rows

Flock will split your DataFrame into chunks, send each chunk to a specific process, and inside each process it will multiprocess each row. This approach is very scalable if you have a very large dataframe and want to perform an apply method.

``` python
from pandas import DataFrame
from flockmp.dataframe import DataFrameAsync


df = DataFrame({"foo": [5, 10, 15, 20],
                "bar": [1, 2, 3, 4]})
df["new-var"] = DataFrameAsync.apply(df[["foo", "bar"]],
                                    lambda x: (x["foo"] + x["bar"]) ** 2, style="row-like")
```



# Installation

Already available in PYPI as:

``` python
pip install flockmp
```



# Contributing

Please, fork the repository and make sure to run all tests before submitting any contribution.

In order to execute all tests for this project, run the command below:


``` python
python setup.py test
```
