# Flock Multiprocessing

Python library for Duck-like multiprocessing 

Flock is intended to help you to easily apply multiprocessing in your development code without thinking too much.

The system is capable of easily setup a multiprocessing environment to handle instance methods, class methods, lambdas and regular functions to be applied to any iterable. See the documentation [Getting Started!](http://flock.readthedocs.io/en/master/starting.html)


When the function to be multiprocessed makes any interaction with **databases** we run into trouble because connections are not allowed to be passed through processes inside messages. In order to handle this situation, we developed the **DatabaseAsync** class, [check it out](http://flock.readthedocs.io/en/master/starting.html#database-dependent-functions)


# Installation

Already available as in pypi

``` python
pip install flockmp
```



# Contributing

Please, fork the repository and make sure to run all tests before submitting any contribution.

In order to execute all tests for this project, run the command below:

``` python
python -m unittest discover test
```
