''' "Python header" for LegTrajectory.h'''

from Coordinates_py cimport Coordinates
from State cimport State
from BaseFrameTrajectory_py cimport BaseFrameTrajectory

cdef extern from "LegTrajectory.cpp": # tell cython that this is the source
    pass

cdef extern from "LegTrajectory.h":
    cdef cppclass LegTrajectory:
        LegTrajectory(State* pstate, BaseFrameTrajectory* pbftrajectory) except +
        Coordinates get_leg_position(float t)