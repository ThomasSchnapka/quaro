''' "Python header" for GaitController.h'''

from Coordinates_py cimport Coordinates

cdef extern from "GaitController.cpp": # tell cython that this is the source
    pass

cdef extern from "GaitController.h":
    cdef cppclass GaitController:
        GaitController() except +
        Coordinates get_leg_position(float t)
        void set_vel_x(float vx)
        void set_cycle_time(float ct)
        void set_support_ratio(float sr)
        void set_phase(float p0, float p1, float p2, float p3)
        void set_swing_hight(float sh)