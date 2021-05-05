"""
3D splines

Splines are stored in a list. This approach is inelegant and perhaps slow
because it relies on loops. Only a workaround for testing.

TODO: Change the above stated flaw 
"""

import numpy as np
from scipy.interpolate import make_interp_spline as spline

class SwingSpline:
    
    def __init__(self, support_ratio, swing_hight, touchdown_pos, liftoff_pos):
        self.support_ratio = support_ratio
        self.midpoint = support_ratio + 0.5*(1-support_ratio)
        self.swing_hight = swing_hight
        
        self.splines = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.change_swing_spline(np.ones(4).astype(bool), touchdown_pos, liftoff_pos)
        
    def get_leg_position(self, t):
        '''retrun 3x4 array with swing positions at time t'''
        pos = np.zeros((3,4))
        for l in range(4):
            pos[0, l] = self.splines[0][l](t[l])
            pos[1, l] = self.splines[1][l](t[l])
            pos[2, l] = self.splines[2][l](t[l])
        return pos
    
    def change_swing_spline(self, to_be_changed, touchdown_pos, liftoff_pos):
        '''change splines defined in to_be_changed (1x4 bool array)'''
        to_be_changed = np.argwhere(to_be_changed).T[0]
        for i in to_be_changed:
            self.splines[0][i] = spline([self.support_ratio, 1], [liftoff_pos[0][i], touchdown_pos[0][i]],
                                        k=3, bc_type="clamped")
            self.splines[1][i] = spline([self.support_ratio, 1], [liftoff_pos[1][i], touchdown_pos[1][i]],
                                        k=3, bc_type="clamped")
            self.splines[2][i] = spline([self.support_ratio, self.midpoint, 1],
                                        [liftoff_pos[2][i], self.swing_hight, touchdown_pos[2][i]],
                                        bc_type="natural")

### module test ###############################################################

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    touchdown_pos = np.array([[20, 20, 20, 20],
                              [ 0,  0,  0,  0],
                              [ 0,  0,  0,  0]]).astype(float)
    liftoff_pos = np.array([[-20,-20,-20,-20],
                            [  0,  0,  0,  0],
                            [  0,  0,  0,  0]]).astype(float)
    
    ss = SwingSpline(0.8, 20, touchdown_pos, liftoff_pos)
    tt = np.linspace(0.7, 1.1, 50)
    pos = np.zeros((3, 50))
    
    for i in range(50):
        pos[:,i] = ss.get_leg_position(tt[i]*np.ones(4))[:,0]
    
    plt.plot(tt, pos[0,:], label="x")
    plt.plot(tt, pos[1,:], label="y")
    plt.plot(tt, pos[2,:], label="z")
    plt.axvline(0.8, color="gray")
    plt.axvline(1, color="gray")
    plt.ylim([-30, 30])
    plt.legend()
    plt.show()
    
    # again with changes to touchdown and liftoff pos
    touchdown_pos = np.zeros((3,4))
    touchdown_pos[0][0] = 20
    touchdown_pos[2][0] = 20
    liftoff_pos = np.zeros((3,4))
    liftoff_pos[0][0] = -20
    liftoff_pos[2][0] = -20
    ss.change_swing_spline(np.array([True, True, False, False]),
                           touchdown_pos, liftoff_pos)
    
    for i in range(50):
        pos[:,i] = ss.get_leg_position(tt[i]*np.ones(4))[:,0]
    
    plt.plot(tt, pos[0,:], label="x")
    plt.plot(tt, pos[1,:], label="y")
    plt.plot(tt, pos[2,:], label="z")
    plt.axvline(0.8, color="gray")
    plt.axvline(1, color="gray")
    plt.ylim([-30, 30])
    plt.legend()
    plt.show()
    