from setuptools import setup, find_packages

__version__ = '1.2.0b5'

setup(name='FlockMP',
      version=__version__,
      description="Python duck-like multiprocessing library",
      url="https://github.com/Captalys/flock",
      author="Wanderson Ferreira & Denis Urbanavicius",
      author_email="wanderson.ferreira@captalys.com.br",
      license="MIT",
      keywords="captalys analitics multiprocessing dataframe",
      package_dir={'flockmp': 'flockmp'},
      packages=["flockmp", "flockmp.base", "flockmp.database", 
                "flockmp.dataframe", "flockmp.list", "flockmp.utils"],
      python_requires='>=3',
      install_requires=[
          'dill',
          'pandas',
          'numpy',
          'tqdm'
      ],
      zip_safe=False,
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ])
