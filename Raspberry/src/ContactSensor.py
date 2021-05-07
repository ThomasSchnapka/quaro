#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 13:42:26 2021

@author: Thomas
"""

import numpy as np

class ContactSensor:
    
    def __init__(self):
        self.leg_state = np.zeros(4).astype(bool)
        pass
    
    def read(self):
        '''return contact sensor reading in 1x4 np bool array'''
        return self.leg_state
        