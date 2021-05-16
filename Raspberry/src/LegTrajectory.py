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
from .cpp.gen_ssp import SwingSpline_py
from .COMTrajectory import COMTrajectory
from .ContactSensor import ContactSensor




class LegTrajectory:
    
    def __init__(self, state, comtraj, contact_sensor):
         # inheritance
         self.state = state
         self.support_ratio = state.support_ratio
         self.phase = state.phase
         self.cycle_time = state.cycle_time
         self.comtraj = comtraj
         self.contact_sensor = contact_sensor
         self.leg_state = state.leg_state
         
         # working varables
         self.liftoff_pos   = np.zeros((3,4))
         self.touchdown_pos = np.zeros((3,4))
         self.com_at_touchdown = np.zeros((3,4))
         self.current_position = np.zeros((3,4))
         
         # finite state machine
         self.fsm = np.zeros(4)         
         self.fsm_last = np.zeros(4)
         
          # modules
         #self.swingSpline = SwingSpline(self.state, self.comtraj, self.liftoff_pos, 0)
         self.swingSpline = SwingSpline_py()
         
         
         
    def get_leg_position(self, t):
        '''returns 3x4 array with leg positions at time t (unnormalized)'''
        
        # normalized time
        t_n = (t/self.cycle_time + self.phase)%1.0
        
        # update statemachine
        self.fsm = self.update_statemachine(self.fsm, t_n)
        fsm_change = (self.fsm != self.fsm_last)
        self.fsm_last = np.copy(self.fsm)
        
        # update trajectories
        self.update_touchdown_points(self.fsm, fsm_change)
        self.update_swing_splines(self.fsm, fsm_change, t)
        
        # set new leg state
        self.leg_state[self.fsm == 0] = True
        self.leg_state[self.fsm != 0] = False
        
        # get new leg positions
        pos = np.zeros((3,4))
        pos[:,self.leg_state] = self.get_position_stance(t)[:,self.leg_state]
        pos[:,~self.leg_state] = self.get_position_swing(t_n)[:,~self.leg_state]
        
        # save position
        self.current_position = np.copy(pos)
        
        return pos
    
    def update_statemachine(self, fsm, t_n):
        '''see doc for finite statemachine
            0 = stance
            1 = ascending
            2 = descending
            '''
        supp = self.support_ratio
        supp_mid = self.support_ratio + 0.5*(1-self.support_ratio)
        csens = self.contact_sensor.read()
        
        fsm[(fsm == 0) & (t_n >= supp)]          = 1
        fsm[(fsm == 1) & (t_n >= supp_mid)]      = 2
        fsm[(fsm == 2) & ((t_n < supp) | csens)] = 0
        
        return fsm
    
    
    def update_touchdown_points(self, fsm, fsm_changed):
        '''set new touchdown points if state change from 2 to 0'''
        new_td = (fsm==0) & fsm_changed
        #curr_com = np.tile(self.state.x_com[:,np.newaxis], 4)
        curr_com = self.comtraj.get_stab_com()
        self.com_at_touchdown[:, new_td] = curr_com[:, new_td]
        self.touchdown_pos[:, new_td] = self.current_position[:, new_td]
        
    
    def update_swing_splines(self, fsm, fsm_change, t):
        '''set new touchdown points if state change from 0 to 1'''
        swing_new = (fsm==1) & fsm_change
        if np.any(swing_new):
            self.liftoff_pos[:, swing_new] = self.current_position[:, swing_new]
            self.create_new_swing_splines(swing_new, t)
            
    
    def predict_leg_position(self, t):
        '''returns Nx3x4 array with leg positions at time t (normalized, N)'''
        pass
    
    
    def get_position_stance(self, t):
        '''returns 3x4 array with leg positions at time t in stance
        legs move against com position!'''
        diff = (self.comtraj.get_stab_com() - self.com_at_touchdown)
        pos = self.touchdown_pos - diff
        return pos
        
    def get_position_swing(self, t_n):
        '''returns 3x4 array with leg positions at time t (normalized, 1x4) in swing'''
        # when moving downwards, check foot contact switch and set touchdown pos
        a = self.swingSpline.get_leg_position(0.0)
        pos = np.ones((3,4))
        return pos
        
    
    def create_new_swing_splines(self, swing_new, t):
        '''changes spline representing swing trajectory'''
        self.swingSpline.change_spline(0, 0, 0)
        self.touchdown_pos[:,swing_new] = np.zeros((3,4))[:,swing_new]
        
