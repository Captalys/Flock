from setuptools import setup
import re
import os
version = '1.0.0'

setup(name='Flock',
      version=version,
      description="Python duck-like multiprocessing library",
      url="https://github.com/Captalys/flock",
      author="Wanderson Ferreira & Denis Urbanavicius",
      author_email="wanderson.ferreira@captalys.com.br",
      license="BSD",
      keywords="captalys analitics",
      packages=["flock"],
      zip_safe=False)
