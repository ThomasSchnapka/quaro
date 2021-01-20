#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 13:28:55 2021

@author: Thomas
"""

import numpy as np
import time

UPDATE_TIME = 30
PUSHUP_AMOUNT = 5
PUSHUP_TIME = 1000.0

def start_demo(controller):
    # pushups
    start_time = current_time()
    last_time = 0
    print "[Demo] starting demo"
    for n in range(PUSHUP_AMOUNT):
        print "[Demo] Pushup Nr.", n+1
        start_time = current_time()
        while (current_time() - start_time) < PUSHUP_TIME:
            if (current_time() - last_time) > 30:
                t = (current_time() - start_time)/PUSHUP_TIME
                position = pushups(t)
                controller.set_leg_position(position)
                last_time = current_time()
    
def pushups(t):
    position = np.zeros((3,4))
    position[2] = 138 + 10*np.sin(2*np.pi*t)
    return position
    
    
def current_time():
    '''return current system time in ms'''
    return int(round(time.time() * 1000))

    