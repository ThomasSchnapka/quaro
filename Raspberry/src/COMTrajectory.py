#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 08:04:06 2021

@author: Thomas
"""

import numpy as np
import time

class COMTrajectory:
    def __init__(self, state, stabilizer):
        self.state      = state
        self.stabilizer = stabilizer
        self.x_com      = state.x_com    # COM position
        self.dx_com     = state.dx_com   # COM velocity
        self.rpy        = state.rpy      # COM rotation
        self.drpy       = state.drpy     # COM rotation velocity
        
        self.x_com_stb  = np.zeros(3)    # stabilized COM position
        self.last_update  = 0
  
        
    def update_state(self, t):
        '''
        change COM position in all 6 DOF
        t is global, unnormalized time
        '''
        dt = (t - self.last_update)
        self.x_com += self.dx_com*dt
        self.x_com_stb = self.x_com + self.stabilizer.stability_shift(t)
        self.rpy += self.drpy*dt
        self.last_update = np.copy(t)
        
        
    def predict_x_com(self, t):
        '''return estimated x aussuming the velocity does not change'''
        x_pred = self.x_com + self.dx_com*(t - self.last_update)
        x_pred += self.stabilizer.stability_shift(t)
        return x_pred
    
    def get_stab_com(self):
        '''return position of stabilized COM in 3x4 array
        is used by leg position'''
        return np.tile(self.x_com_stb[:,np.newaxis], 4)