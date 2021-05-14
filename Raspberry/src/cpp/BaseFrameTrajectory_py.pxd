''' "Python header" for BaseFrameTrajectory.h'''

from State cimport State

cdef extern from "BaseFrameTrajectory.cpp": # tell cython that this is the source
    pass

cdef extern from "BaseFrameTrajectory.h":
    cdef cppclass BaseFrameTrajectory:
        BaseFrameTrajectory(State* pstate) except +
        void update(float t)