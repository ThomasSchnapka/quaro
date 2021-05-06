#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 08:04:06 2021

@author: Thomas
"""

import numpy as np

class COMTrajectory:
    def __init__(self, state):
        self.state     = state
        self.x_com     = state.x_com    # COM position
        self.dx_com    = state.dx_com   # COM velocity
        self.rpy       = state.rpy      # COM rotation
        self.drpy      = state.drpy     # COM rotation velocity
        self.last_time = 0
        
    def update_state(self, t):
        '''
        change COM position in all 6 DOF
        t is global, unnormalized time
        '''
        dt = (t - self.last_time)
        self.x_com += self.dx_com*dt
        self.rpy += self.drpy*dt
        self.last_time = t
    