cdef extern from "SwingSpline.cpp": # tell cython that this is the source
    pass

# Declare the class with cdef
cdef extern from "SwingSpline.h" namespace "quaro":
    cdef cppclass SwingSpline:
        SwingSpline() except +
        int get_leg_position(float t)
        void change_spline(int, int, int)