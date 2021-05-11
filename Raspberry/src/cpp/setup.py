# run setup.py build_ext --inplace

from setuptools import setup

from Cython.Build import cythonize

'''
setup(ext_modules=cythonize("gen_ssp.pyx",
                            include_path=["eigen-3.4-rc1"])
      )
'''

setup(ext_modules=cythonize("SwingSpline_py.pyx"), annotate=True)