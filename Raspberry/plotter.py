'''
small script to plt gait coordinates
'''

from src.State import State
from quaro.HardwareConfig import HardwareConfig
from src.GaitController import GaitController

import numpy as np
import matplotlib.pyplot as plt
import time


hardware_config = HardwareConfig()
state = State()

gait_controller = GaitController(state, hardware_config)

plot_time = 1500
coordinates = np.zeros((1,3))

def current_time():
        '''return current system time in ms'''
        return int(round(time.time() * 1000))

def update_leg_position(coordinates):
    '''check if leg positions need to be updated, calculate and send them'''
    position = gait_controller.get_position()
    if position is not None:
        # save coordinates of first leg
        coordinates = np.vstack((coordinates, position[:,0]))
    return coordinates

print "capturing coordinates for " + str(plot_time) + "ms"
start_time = current_time()
while current_time() - start_time < plot_time:
    coordinates = update_leg_position(coordinates)
    
# remove first item which was a placeholder
coordinates = coordinates[1:]

plt.suptitle("absolute coordinates of leg 0")
plt.subplot(1, 2, 1, ylabel="dist [mm]", xlabel="measured points",)
plt.plot(coordinates[:,0], label="x")
plt.plot(coordinates[:,1], label="y")
plt.legend()
plt.subplot(1, 2, 2, ylabel="dist [mm]", xlabel="measured points",)
plt.plot(coordinates[:,2], label="z")
plt.legend()
    

        
    