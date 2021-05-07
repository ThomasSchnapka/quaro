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
from src.COMTrajectory import COMTrajectory
from src.LegTrajectory import LegTrajectory
from src.ContactSensor import ContactSensor

s = State()
ct = COMTrajectory(s)
cs = ContactSensor()
lt = LegTrajectory(s, ct, cs)


N = 200
pos = np.zeros((3,4,N))
t_idx = np.linspace(0, 5 , N)
for i in range(N):
    if t_idx[i] > 0.69:
        cs.leg_state[3] = True
    if t_idx[i] > 0.72:
        cs.leg_state[3] = False
    ct.update_state(t_idx[i])
    pos[:,:,i] = lt.get_leg_position(t_idx[i])

for i in [3]:#range(4):
    plt.plot(t_idx, pos[0, i, :], label=("x"+str(i)))
    plt.plot(t_idx, pos[1, i, :], label=("y"+str(i)))
    plt.plot(t_idx, pos[2, i, :], label=("z"+str(i)))
    
plt.legend()
#plt.ylim([-0.5, 0.5])