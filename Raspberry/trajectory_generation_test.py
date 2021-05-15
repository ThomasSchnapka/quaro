#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 08:19:55 2021

@author: Thomas
"""

import matplotlib.pyplot as plt
import numpy as np
'''
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
'''

from src.Stabilizer import Stabilizer
from src.cpp.LegTrajectory_py import LegTrajectory_py

lt = LegTrajectory_py()
lt.set_vel_x(0.0)
lt.set_support_ratio(0.7)

N = 1000
pos = np.zeros((3,4,N))
t_idx = np.linspace(0, 10, N)
for i in range(N):
    #if i==N/4:
     #   
    #    print("changed ct at", t_idx[i])
    lt.update_com(t_idx[i])
    pos[:,:,i] = lt.get_leg_position(t_idx[i])

for i in [0, 1]:#range(4):
    plt.plot(t_idx, pos[0, i, :], label=("x"+str(i)))
    plt.plot(t_idx, pos[1, i, :], label=("y"+str(i)))
    plt.plot(t_idx, pos[2, i, :], label=("z"+str(i)))

#plt.plot(t_idx, np.sum(pos[0, :, :], axis=0), label=("x"+str(i)))
    
plt.legend()
#plt.ylim([-0.5, 0.5])