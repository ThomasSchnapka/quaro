"""
Contains functions to maintain static and dynamic stabiliy
"""

import numpy as np

class Stabilizer:
    '''containins all methods concering dynamic and static stability'''
    
    def __init__(self, state):
        self.state = state
        
    def stabilize_gait(self, leg_state, leg_time, position):
        '''
        calculates how the current leg positions habe to be altered
        in order to ensure that there is a certain stability margin
        (distance from COM to support triangle)
        
        Args:
            leg_state: 4x1 bool if leg is supporting or not
            leg_time: 4x1 array with normalized leg times
            position: 4x3 array with current leg positions
        Returns:
            4x3 array with stabilized absolute leg positions
        '''
        
        # TODO add calculation based on old robot
        return position