# distutils: language = c++

from SwingSpline cimport SwingSpline

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef class SwingSpline_py:
    cdef SwingSpline ssp # Hold a C++ instance which we're wrapping

    def __cinit__(self):
        self.ssp = SwingSpline()
    
    def get_leg_position(self, float t):
        return self.ssp.get_leg_position(t)
    
    def change_spline(self, int to_be_changed, int liftoff_pos, int t):
        return self.ssp.change_spline(to_be_changed, liftoff_pos, t)