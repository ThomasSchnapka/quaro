"""
Tests of the trajectory generation for profiling and trajectory optimization

Plots the leg trajectories using the current gait generator
"""

import matplotlib.pyplot as plt
import numpy as np
from src.cpp.GaitController_py import GaitController_py

# imports and settings
gc = GaitController_py()
gc.set_cycle_time(1.5)
gc.set_support_ratio(0.7)
gc.set_phase(0, 0.25, 0.5, 0.75)
gc.set_swing_hight(0.02)

# plot
N = 1000
pos = np.zeros((3,4,N))
t_idx = np.linspace(0, 3, N)
for i in range(N):
    pos[:,:,i] = gc.get_leg_position(t_idx[i])

for i in [0, 1]:#range(4):
    plt.plot(t_idx, pos[0, i, :], label=("x"+str(i)))
    plt.plot(t_idx, pos[1, i, :], label=("y"+str(i)))
    plt.plot(t_idx, pos[2, i, :], label=("z"+str(i)))


plt.grid()
plt.legend()