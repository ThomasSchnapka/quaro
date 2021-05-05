#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class containing the leg trajecory function, parametrizable, for each leg 
individually

swing phase controlled here,
stance adopts COM trajectory class

TODO:
    implement foot_contact_sensor_reading for tests
"""

import numpy as np
from SwingSpline import SwingSpline


# for testing
contact_sensor_reading = np.array([0, 0, 0, 0]).astype(bool)

class LegTrajectory:
    
    def __init__(self, support_ratio):
         # TODO: inherit setting from state
         self.support_ratio = 0.8
         self.operating_hight = 180
         self.last_t = np.zeros(4)
         self.touchdown_pos = np.array([[20, 20, 20, 20],
                                        [ 0,  0,  0,  0],
                                        [ 0,  0,  0,  0]]).astype(float)
         self.liftoff_pos = np.array([[-20,-20,-20,-20],
                                      [  0,  0,  0,  0],
                                      [  0,  0,  0,  0]]).astype(float)
         self.leg_state = np.array([1, 1, 1, 1]).astype(bool) # supporting or not
         self.current_position = np.zeros((3, 4))
         self.swingSpline = SwingSpline(support_ratio, 30,
                                        self.touchdown_pos, self.liftoff_pos)
         
    def get_leg_position(self, t):
        '''returns 3x4 array with leg positions at time t (normalized)'''
        # check if leg was swinging and has contact for first time
        contact_new = ~self.leg_state & contact_sensor_reading
        self.touchdown_pos[:,contact_new] = self.current_position[:,contact_new]
        
        # create new swing splines if necessary
        swing_new = ~self.leg_state & (t >= self.support_ratio)
        if np.any(swing_new):
            self.create_new_swing_splines(swing_new)
        
        # set new supporting status
        # hier fehlt einfluss von contact new
        #self.leg_state = np.logical_or(self.leg_state, t >= self.support_ratio)
        # Ausweichloesung:
        self.leg_state[(t >= self.support_ratio)
                        & (self.last_t <= self.support_ratio)] = False
        self.leg_state[(t <= self.support_ratio) | contact_new] = True
        
        # get new leg positions
        pos = np.zeros((3,4))
        pos[:,self.leg_state] = ( self.get_position_stance(t)[:,self.leg_state]
                                + self.touchdown_pos[:,self.leg_state])
        pos[:,~self.leg_state] = self.get_position_swing(t)[:,~self.leg_state]
        
        # save position
        self.current_position = pos
        self.last_t = t
        
        return pos
    
    def predict_leg_position(self, t):
        '''returns Nx3x4 array with leg positions at time t (normalized, N)'''
        pass
    
    def get_position_stance(self, t):
        '''returns 3x4 array with leg positions at time t (normalized) in stance'''
        # TODO: change global COM position into local leg position
        pos = np.zeros((3,4))
        pos[0,:] = pos[0,:] - t*40/self.support_ratio
        return pos
        
    def get_position_swing(self, t):
        '''returns 3x4 array with leg positions at time t (normalized) in swing'''
        # when moving downwards, check foot contact switch and set touchdown pos
        pos = self.swingSpline.get_leg_position(t)
        return pos
        
    def create_new_swing_splines(self, swing_new):
        '''changes spline representing swing trajectory'''
        self.swingSpline.change_swing_spline(swing_new,
                                             self.touchdown_pos,
                                             self.liftoff_pos)
        
### module test ###############################################################

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    lt = LegTrajectory(0.8)
    N = 100
    pos = np.zeros((3,4,N))
    t_idx = np.linspace(0, 1, N)
    t = np.tile(np.array([0, 0.25, 0.5, 0.75]), (N,1)) + np.tile(t_idx, (4, 1)).T 
    t = t%1
    for i in range(N):
        if i==N*0.48:
            contact_sensor_reading = np.array([0, 0, 1, 0]).astype(bool)
        pos[:,:,i] = lt.get_leg_position(t[i, :])
    
    for i in range(4):
        plt.plot(t_idx, pos[0, i, :], label=("x"+str(i)))
        plt.plot(t_idx, pos[1, i, :], label=("y"+str(i)))
        plt.plot(t_idx, pos[2, i, :], label=("z"+str(i)))
        
    plt.legend()