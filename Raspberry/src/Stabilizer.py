"""
Contains functions to maintain static and dynamic stabiliy
"""

import numpy as np

class Stabilizer:
    '''containins all methods concering dynamic and static stability'''
    
    def __init__(self, state, hardware_config):
        self.state = state
        self.cyc_time = state.cycle_time
        self.stab_amp = self.state.stability_amplitude
        self.hardware_config = hardware_config
        
    def stability_shift(self, t):
        '''
        TODO
        '''
        
        shift_x = np.sin(((t/self.cyc_time) + 1/8)*2*np.pi)
        shift_y = np.cos(((t/self.cyc_time) + 1/8)*2*np.pi)
        
        shift_tot = np.zeros((3,4))
        shift_tot[0] = -shift_x*self.state.stability_amplitude
        shift_tot[1] = -shift_y*self.state.stability_amplitude

        return shift_tot
    