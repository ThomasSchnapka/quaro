import numpy as np
from Coordinates_py cimport Coordinates
from GaitController_py cimport GaitController

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef class GaitController_py:
    #cdef LegTrajectory(State*, COMTrajectory*) lt# Hold a C++ instance which we're wrapping
    #the following classes do not have nullary constructors, so we have to manually allocate them

    cdef GaitController* gc

    def __cinit__(self):
        self.gc = new GaitController()
    
    def get_leg_position(self, float t):
        cdef Coordinates inp = self.gc.get_leg_position(t)
        cdef int i, j
        
        out = np.zeros((3,4))
        for i in range(3):
            for j in range(4):
                out[i, j] = inp(i, j)
        return out
        
    def set_vel_x(self, float vx):
        self.gc.set_vel_x(vx)
        
    def set_cycle_time(self, float ct):
        self.gc.set_cycle_time(ct)
        
    def set_support_ratio(self, float sr):
        self.gc.set_support_ratio(sr)
        
    def set_phase(self, float p0, float p1, float p2, float p3):
        self.gc.set_phase(p0, p1, p2, p3)
    
    def set_swing_hight(self, float sh):
        self.gc.set_swing_hight(sh)