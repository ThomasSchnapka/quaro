''' "Python header" for COMTrajectory.h'''

from State cimport State

cdef extern from "COMTrajectory.cpp": # tell cython that this is the source
    pass

cdef extern from "COMTrajectory.h":
    cdef cppclass COMTrajectory:
        COMTrajectory(State* pstate) except +
        void update(float t)