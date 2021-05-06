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
from .SwingSpline import SwingSpline


# for testing
contact_sensor_reading = np.array([0, 0, 0, 0]).astype(bool)

class LegTrajectory:
    
    def __init__(self, state):
         # TODO: inherit setting from state
         self.state = state
         self.support_ratio = state.support_ratio
         self.operating_hight = state.operating_hight
         self.phase = state.phase
         self.cycle_time = state.cycle_time
         self.last_t_n = np.zeros(4)
         self.touchdown_pos = np.array([[0.01, 0.01, 0.01, 0.01],
                                        [ 0,  0,  0,  0],
                                        [ 0,  0,  0,  0]]).astype(float)
         self.liftoff_pos = np.array([[-0.01,-0.01,-0.01,-0.01],
                                      [  0,  0,  0,  0],
                                      [  0,  0,  0,  0]]).astype(float)
         self.com_at_touchdown = np.zeros((3,4))
         self.leg_state = np.array([1, 1, 1, 1]).astype(bool) # supporting or not
         self.current_position = np.zeros((3, 4))
         self.swingSpline = SwingSpline(state,
                                        self.touchdown_pos, self.liftoff_pos)
         
    def get_leg_position(self, t):
        '''returns 3x4 array with leg positions at time t (unnormalized)'''
        # normalized time
        t_n = (t/self.cycle_time + self.phase)%1
        
        # check for touchdown detected by sensors
        contact_sensor = (~self.leg_state & contact_sensor_reading)
        self.touchdown_pos[:,contact_sensor] = self.current_position[:, contact_sensor]
        self.com_at_touchdown[:,contact_sensor] = np.tile(self.state.x_com[:,np.newaxis], 4)[:,contact_sensor]
        
        # check for touchdown by schedule
        contact_schedule = (~self.leg_state & (t_n <= self.support_ratio))
        ### TODO
        ### COM wird zu frueh gespeichert bei kleinen sampling raten.
        ### prediction o.ae. einbauen
        self.com_at_touchdown[:,contact_schedule] = np.tile(self.state.x_com[:,np.newaxis], 4)[:,contact_schedule]
        self.com_at_touchdown[2,contact_schedule] = 0
        
       
        
        # create new swing splines if necessary
        #swing_new = ~self.leg_state & (t >= self.support_ratio)
        swing_new = self.leg_state & (t_n >= self.support_ratio)
        if np.any(swing_new):
            self.liftoff_pos[:, swing_new] = self.current_position[:, swing_new]
            self.create_new_swing_splines(swing_new)
        
        # set new supporting status
        self.leg_state[(t_n >= self.support_ratio)
                        & (self.last_t_n <= self.support_ratio)] = False
        self.leg_state[(t_n <= self.support_ratio) | contact_sensor] = True
        
        
        # get new leg positions
        pos = np.zeros((3,4))
        pos[:,self.leg_state] = ( self.touchdown_pos[:,self.leg_state]
                                - self.get_position_stance(t)[:,self.leg_state])
        pos[:,~self.leg_state] = self.get_position_swing(t_n)[:,~self.leg_state]
        
        # save position
        self.current_position = pos
        self.last_t_n = t_n
        
        return pos
    
    def predict_leg_position(self, t):
        '''returns Nx3x4 array with leg positions at time t (normalized, N)'''
        pass
    
    def get_position_stance(self, t):
        '''returns 3x4 array with leg positions at time t in stance'''
        # TODO: change global COM position into local leg position
        pos = np.tile(self.state.x_com[:,np.newaxis], 4) - self.com_at_touchdown
        return pos
        
    def get_position_swing(self, t):
        '''returns 3x4 array with leg positions at time t (normalized, 1x4) in swing'''
        # when moving downwards, check foot contact switch and set touchdown pos
        pos = self.swingSpline.get_leg_position(t)
        return pos
        
    def create_new_swing_splines(self, swing_new):
        '''changes spline representing swing trajectory'''
        self.swingSpline.change_swing_spline(swing_new,
                                             self.touchdown_pos,
                                             self.liftoff_pos)
        
