# distutils: language = c++
# distutils: include_dirs = eigen-3.4-rc1
# cython: language_level=3

from SwingSpline cimport SwingSpline
import numpy as np
from Coordinates_py cimport Coordinates

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef class SwingSpline_py:
    cdef SwingSpline ssp # Hold a C++ instance which we're wrapping

    def __cinit__(self):
        self.ssp = SwingSpline()
    

    def get_leg_position(self, float t):
        cdef Coordinates inp = self.ssp.get_leg_position(t)
        cdef int i, j
        
        out = np.zeros((3,4))
        for i in range(3):
            for j in range(4):
                out[i, j] = inp(i, j)
        return out

    
    def change_spline(self, int to_be_changed, int liftoff_pos, int t):
        return self.ssp.change_spline(to_be_changed, liftoff_pos, t)