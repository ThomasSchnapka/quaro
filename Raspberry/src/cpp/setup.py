# run setup.py build_ext --inplace

from setuptools import setup

from Cython.Build import cythonize

setup(ext_modules=cythonize("gen_ssp.pyx"))