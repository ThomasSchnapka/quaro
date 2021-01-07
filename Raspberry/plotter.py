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

# Parameters
plot_time = 1500

coordinates = np.zeros((3,4,1))

def current_time():
        '''return current system time in ms'''
        return int(round(time.time() * 1000))

def update_leg_position(coordinates):
    '''check if leg positions need to be updated, calculate and send them'''
    position = gait_controller.get_position()
    if position is not None:
        # save coordinates of first leg
        coordinates = np.concatenate((coordinates, position[:,:,np.newaxis]),
                                     axis=2)
    return coordinates

print "capturing coordinates for " + str(plot_time) + "ms..."
start_time = current_time()
while current_time() - start_time < plot_time:
    coordinates = update_leg_position(coordinates)
    
# remove first item which was a placeholder
coordinates = coordinates[:,:,1:]

# Plotting

plt.figure(figsize=(10,18))
for leg in range(4):
    plt.subplot(3, 2, (leg+1), ylabel="dist [mm]", xlabel="measured points",
                title=("coordinates of leg " + str(leg)))
    plt.plot(coordinates[0,leg,:], label="x")
    plt.plot(coordinates[1,leg,:], label="y")
    plt.legend()
    
for leg in range(4):
    plt.subplot(3, 2, 5, ylabel="dist [mm]", xlabel="measured points",)
    plt.plot(coordinates[2,leg,:], label=("z" + str(leg)))
    plt.legend()
    

        
    