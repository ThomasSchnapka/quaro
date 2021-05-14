import numpy as np
from Coordinates_py cimport Coordinates
from LegTrajectory_py cimport LegTrajectory
from State_py cimport State
from BaseFrameTrajectory_py cimport BaseFrameTrajectory

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef class LegTrajectory_py:
    #cdef LegTrajectory(State*, COMTrajectory*) lt# Hold a C++ instance which we're wrapping
    #the following classes do not have nullary constructors, so we have to manually allocate them
    cdef State st
    cdef BaseFrameTrajectory* bft
    cdef LegTrajectory* lt

    def __cinit__(self):
        self.st = State()
        self.bft = new BaseFrameTrajectory(&self.st)
        self.lt = new LegTrajectory(&self.st, self.bft)
    
    def get_leg_position(self, float t):
        cdef Coordinates inp = self.lt.get_leg_position(t)
        cdef int i, j
        
        out = np.zeros((3,4))
        for i in range(3):
            for j in range(4):
                out[i, j] = inp(i, j)
        return out
    
    def update_com(self, float t):
        '''helper to update COM position to avoid linking an outside COM trajectory
        object with leg trajectory'''
        self.bft.update(t)
        
    def set_vel_x(self, float vx):
        # TODO: shift this to own State pyx
        self.st.set_vel_x(vx)
        
    def set_cycle_time(self, float ct):
        # TODO: shift this to own State pyx
        self.st.set_cycle_time(ct)
        
    def set_support_ratio(self, float sr):
        # TODO: shift this to own State pyx
        self.st.set_support_ratio(sr)
        