# run setup.py build_ext --inplace

from setuptools import Extension, setup

from Cython.Build import cythonize

'''
setup(ext_modules=cythonize("gen_ssp.pyx",
                            include_path=["eigen-3.4-rc1"])
      )
'''

#setup(ext_modules=cythonize("LegTrajectory_py.pyx"))


extensions = [Extension(name = "LegTrajectory_py", 
                        sources=["LegTrajectory_py.pyx", \
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
'''    
setup(
    ext_modules = [
    Extension("cyproject", 
              sources=["cyproject.pyx", \
                       "adapter/ALabSimulatorBase.cpp", \
                       "adapter/ALabSimulatorTime.cpp", \
                       "adapter/ALabNetBinding.cpp", \
                       "adapter/AValueArg.cpp", \
                       "adapter/ALabSiteSetsManager.cpp", \
                       "adapter/ALabSite.cpp", \
                       ],
              libraries=["cproject"],
              language="c++",
              extra_compile_args=["-I../inc", "-I../../../DEPENDENCIES/python2.7/inc", "-I../../../DEPENDENCIES/gsl-1.8/include"], 
              extra_link_args=["-L../lib"]
              extra_compile_args=["-fopenmp", "-O3"],
              extra_link_args=[]
              )
    ]
)
'''