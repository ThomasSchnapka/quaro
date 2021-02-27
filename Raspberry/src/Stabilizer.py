"""
Contains functions to maintain static and dynamic stabiliy
"""

import numpy as np

class Stabilizer:
    '''containins all methods concering dynamic and static stability'''
    
    def __init__(self, state, hardware_config):
        self.state = state
        self.hardware_config = hardware_config
        
    def stability_shift(self, leg_time):
        '''
        calculated the distance the leg should be shifted in x/y-direction in
        order to keep the COM in the stability triangle
        
        Works independent of gate as it is based on eachs legs individual phase
        
        The way this works is kinda complicated, thus the annotations are not
        very helpful. Please take a look at the docs. Basically, the code
        shifts the COM in the opposite direction of each leg that is not in
        support phase
        
        Args:
            leg_time: 4x1 array with normalized leg times
            position: 4x3 array with current normalized leg positions
        Returns:
            1x3 array with distance each leg should be shifted
        '''
        
        ## first part: calculate length of shift
        # temporal difference between support phase and stability ratio
        stability_overlap = 0.5*(self.state.stability_ratio 
                                 - (1-self.state.support_ratio))
        # shift the leg time by above difference for further calculations
        d = ((leg_time - stability_overlap) - (1 - self.state.stability_ratio))%1
        d /= self.state.stability_ratio
        # create sinus signal in stability phase
        d = self.state.stability_amplitude*np.sin(np.pi*d)
        # delete all entrys for legs that are in support phase
        d[(leg_time - stability_overlap)%1 < (1 - self.state.stability_ratio)] = 0
        
        ## second part: calculate direction of shift
        normalized_leg_location = (self.hardware_config.leg_location
                                   /np.linalg.norm(self.hardware_config.leg_location, axis=0))
        shift_per_leg = np.multiply(d, normalized_leg_location)
        shift_combined = np.sum(shift_per_leg, axis=1)
        # create (3,4) matrix
        shift_combined = np.repeat(shift_combined, 4)
        shift_combined = shift_combined.reshape((3,4))

        return shift_combined