''' "Python header" for SwingSpline.h'''

from Coordinates_py cimport Coordinates

cdef extern from "SwingSpline.cpp": # tell cython that this is the source
    pass

cdef extern from "SwingSpline.h":
    cdef cppclass SwingSpline:
        SwingSpline() except +
        Coordinates get_leg_position(float t)
        void change_spline(int, int, int)