"""
3D splines

Splines are stored in a list. This approach is inelegant and perhaps slow
because it relies on loops. Only a workaround for testing.

TODO: Change the above stated flaw 
"""

import numpy as np
from scipy.interpolate import make_interp_spline as spline

class SwingSpline:
    
    def __init__(self, state, comtraj, liftoff_pos, t_init):
        self.state = state
        self.comtraj = comtraj
        self.support_ratio = state.support_ratio
        self.midpoint = self.support_ratio + 0.5*(1-self.support_ratio)
        self.swing_hight = state.swing_hight
        
        self.splines = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.change_spline(np.ones(4).astype(bool), liftoff_pos, t_init)
        
    def get_leg_position(self, t):
        '''retrun 3x4 array with swing positions at normalzed time t (1x4)'''
        pos = np.zeros((3,4))
        for l in range(4):
            pos[0, l] = self.splines[0][l](t[l])
            pos[1, l] = self.splines[1][l](t[l])
            pos[2, l] = self.splines[2][l](t[l])
        return pos
    
    def change_spline(self, to_be_changed, liftoff_pos, t):
        '''change splines defined in to_be_changed (1x4 bool array)
        retrun new touchdown position'''
        to_be_changed = np.argwhere(to_be_changed).T[0]
        
        # calculate new optimal touchdown position
        t_touchdown   = t + self.state.cycle_time*(1.0 - self.support_ratio)
        touchdown_pos = self.comtraj.predict_x_com(t_touchdown)
        touchdown_pos = np.tile(touchdown_pos[:,np.newaxis], 4)
        touchdown_pos = (touchdown_pos - self.comtraj.get_stab_com())*0.5
        
        # create new splines
        for i in to_be_changed:
            self.splines[0][i] = spline([self.support_ratio, 1],
                                        [liftoff_pos[0][i], touchdown_pos[0][i]],
                                        k=3, bc_type="clamped")
            self.splines[1][i] = spline([self.support_ratio, 1],
                                        [liftoff_pos[1][i], touchdown_pos[1][i]],
                                        k=3, bc_type="clamped")
            self.splines[2][i] = spline([self.support_ratio, self.midpoint, 1],
                                        [liftoff_pos[2][i], self.swing_hight, touchdown_pos[2][i]],
                                        bc_type="natural")
            
        return touchdown_pos[:,to_be_changed]


    