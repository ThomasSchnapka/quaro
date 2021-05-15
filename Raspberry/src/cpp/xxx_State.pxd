''' "Python header" for State.h'''


cdef extern from "State.cpp": # tell cython that this is the source
    pass

cdef extern from "State.h":
    cdef cppclass State:
        State() except +