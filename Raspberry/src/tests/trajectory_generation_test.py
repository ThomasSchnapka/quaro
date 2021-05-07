#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 08:19:55 2021

@author: Thomas
"""

import matplotlib.pyplot as plt
import numpy as np
import time
from src.State import State
from COMTrajectory import COMTrajectory
from LegTrajectory import LegTrajectory

s = State()
ct = COMTrajectory(s)
lt = LegTrajectory(s)


N = 100
pos = np.zeros((3,4,N))
t_idx = np.linspace(0, 2 , N)
phase = np.array([0, 0.25, 0.5, 0.75])
for i in range(N):
    if i==N*0.48:
        contact_sensor_reading = np.array([0, 0, 1, 0]).astype(bool)
    ct.update_state(t_idx[i])
    tt = phase + t_idx[i]*np.ones(4)
    pos[:,:,i] = lt.get_leg_position(tt)

for i in range(4):
    plt.plot(t_idx, pos[0, i, :], label=("x"+str(i)))
    plt.plot(t_idx, pos[1, i, :], label=("y"+str(i)))
    plt.plot(t_idx, pos[2, i, :], label=("z"+str(i)))
    
plt.legend()