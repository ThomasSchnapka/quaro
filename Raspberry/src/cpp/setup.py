'''
Cython setup file
'''

# run setup.py build_ext --inplace

from setuptools import Extension, setup

from Cython.Build import cythonize

extensions = [Extension(name = "GaitController_py", 
                        sources=["GaitController_py.pyx", \
                                 "State.cpp",\
                                 "BaseFrameTrajectory.cpp",\
                                 "LegTrajectory.cpp",\
                                 "SingleLegTrajectory.cpp",\
                                 "SwingSpline.cpp",\
                                 "ContactSensor.cpp"\
                                 ],
                            include_dirs=["eigen-3.4-rc1"],
                            language="c++"
                            )
              ]

setup(
    ext_modules=cythonize(extensions,
                          compiler_directives={'language_level' : "3"})
)