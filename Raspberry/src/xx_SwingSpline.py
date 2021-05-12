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
        
        self.splines0x = 0
        self.splines1x = 0
        self.splines2x = 0
        self.splines3x = 0
        self.splines0y = 0
        self.splines1y = 0
        self.splines2y = 0
        self.splines3y = 0
        self.splines0z = 0
        self.splines1z = 0
        self.splines2z = 0
        self.splines3z = 0
        
        self.change_spline(np.ones(4).astype(bool), liftoff_pos, t_init)
         
    def get_leg_position(self, t):
        '''retrun 3x4 array with swing positions at normalzed time t (1x4)'''
        pos = np.zeros((3,4), np.float32)
        '''
        for l in range(4):
            pos[0, l] = self.splines[0][l](t[l])
            pos[1, l] = self.splines[1][l](t[l])
            pos[2, l] = self.splines[2][l](t[l])
        '''
        pos[0, 0] = self.splines0x(t[0], extrapolate=None)
        pos[1, 0] = self.splines0y(t[0], extrapolate=None)
        pos[2, 0] = self.splines0z(t[0], extrapolate=None)
        pos[0, 1] = self.splines1x(t[1], extrapolate=None)
        pos[1, 1] = self.splines1y(t[1], extrapolate=None)
        pos[2, 1] = self.splines1z(t[1], extrapolate=None)
        pos[0, 2] = self.splines2x(t[2], extrapolate=None)
        pos[1, 2] = self.splines2y(t[2], extrapolate=None)
        pos[2, 2] = self.splines2z(t[2], extrapolate=None)
        pos[0, 3] = self.splines3x(t[3], extrapolate=None)
        pos[1, 3] = self.splines3y(t[3], extrapolate=None)
        pos[2, 3] = self.splines3z(t[3], extrapolate=None)
        
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
        '''
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
        '''
        # x
        self.splines0x = spline([self.support_ratio, 1],
                                [liftoff_pos[0][0], touchdown_pos[0][0]],
                                k=3, bc_type="clamped")
        self.splines1x = spline([self.support_ratio, 1],
                                [liftoff_pos[0][1], touchdown_pos[0][1]],
                                k=3, bc_type="clamped")
        self.splines2x = spline([self.support_ratio, 1],
                                [liftoff_pos[0][2], touchdown_pos[0][2]],
                                k=3, bc_type="clamped")
        self.splines3x = spline([self.support_ratio, 1],
                                [liftoff_pos[0][3], touchdown_pos[0][3]],
                                k=3, bc_type="clamped")
        # y
        self.splines0y = spline([self.support_ratio, 1],
                                        [liftoff_pos[1][0], touchdown_pos[1][0]],
                                        k=3, bc_type="clamped")
        self.splines1y = spline([self.support_ratio, 1],
                                        [liftoff_pos[1][1], touchdown_pos[1][1]],
                                        k=3, bc_type="clamped")
        self.splines2y = spline([self.support_ratio, 1],
                                        [liftoff_pos[1][2], touchdown_pos[1][2]],
                                        k=3, bc_type="clamped")
        self.splines3y = spline([self.support_ratio, 1],
                                        [liftoff_pos[1][3], touchdown_pos[1][3]],
                                        k=3, bc_type="clamped")
        # z
        self.splines0z = spline([self.support_ratio, self.midpoint, 1],
                                        [liftoff_pos[2][0], self.swing_hight, touchdown_pos[2][0]],
                                        bc_type="natural")
        self.splines1z = spline([self.support_ratio, self.midpoint, 1],
                                        [liftoff_pos[2][1], self.swing_hight, touchdown_pos[2][1]],
                                        bc_type="natural")
        self.splines2z = spline([self.support_ratio, self.midpoint, 1],
                                        [liftoff_pos[2][2], self.swing_hight, touchdown_pos[2][2]],
                                        bc_type="natural")
        self.splines3z = spline([self.support_ratio, self.midpoint, 1],
                                        [liftoff_pos[2][3], self.swing_hight, touchdown_pos[2][3]],
                                        bc_type="natural")
            
        return touchdown_pos[:,to_be_changed]


    