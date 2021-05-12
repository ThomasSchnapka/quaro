''' "Python header" for LegTrajectory.h'''

from Coordinates_py cimport Coordinates
from State cimport State
from COMTrajectory_py cimport COMTrajectory

cdef extern from "LegTrajectory.cpp": # tell cython that this is the source
    pass

cdef extern from "LegTrajectory.h":
    cdef cppclass LegTrajectory:
        #cdef cppclass State
        #cdef cppclass COMTrajectory
        LegTrajectory(State* pstate, COMTrajectory* pcomtrajectory) except +
        Coordinates get_leg_position(float t)