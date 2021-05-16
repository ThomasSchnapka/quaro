''' "Python header" for Coordinates.h'''

cdef extern from "Coordinates.h":
    cdef cppclass Coordinates:
        Coordinates() except +
        float operator()(int, int)