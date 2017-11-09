from setuptools import setup

__version__ = '1.0.0'

setup(name='Flock',
      version=__version__,
      description="Python duck-like multiprocessing library",
      url="https://github.com/Captalys/flock",
      author="Wanderson Ferreira & Denis Urbanavicius",
      author_email="wanderson.ferreira@captalys.com.br",
      license="BSD",
      keywords="captalys analitics",
      packages=["flock"],
      install_requires=[
          'dill',
          'pandas',
          'numpy'
      ],
      zip_safe=False)
