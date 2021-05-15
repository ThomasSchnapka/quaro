''' "Python header" for State.h'''


cdef extern from "State.cpp": # tell cython that this is the source
    pass

cdef extern from "State.h":
    cdef cppclass State:
        State() except +
        void set_vel_x(float vx)
        void set_cycle_time(float ct)
        void set_support_ratio(float sr)
        void set_phase(float p0, float p1, float p2, float p3)
        void set_swing_hight(float sh)