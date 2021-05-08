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
from src.Stabilizer import Stabilizer
from src.ContactSensor import ContactSensor

state = State()
stabilizer = Stabilizer(state)
ct = COMTrajectory(state, stabilizer)
cs = ContactSensor()
lt = LegTrajectory(state, ct, cs)


N = 200
pos = np.zeros((3,4,N))
t_idx = np.linspace(0, 5, N)
for i in range(N):
    ct.update_state(t_idx[i])
    pos[:,:,i] = lt.get_leg_position(t_idx[i])

for i in range(4):
    plt.plot(t_idx, pos[0, i, :], label=("x"+str(i)))
    plt.plot(t_idx, pos[1, i, :], label=("y"+str(i)))
    plt.plot(t_idx, pos[2, i, :], label=("z"+str(i)))

#plt.plot(t_idx, np.sum(pos[0, :, :], axis=0), label=("x"+str(i)))
    
plt.legend()
#plt.ylim([-0.5, 0.5])