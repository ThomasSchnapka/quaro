import numpy as np
import time

from .SwingController import SwingController
from .SupportController import SupportController
from .TouchdownLocalizer import TouchdownLocalizer
from .Stabilizer import Stabilizer


class GaitController:
    '''
    Decides wether leg is swinging or supporting, calculates their normalized
    coordinates and maps them to absolute ones
    
    Info regarding normalized leg positions: the z-position is considered 1 if 
    all angles are zero (leg is fully streched out). z-position of the shoulder
    joint is 0, which means that the distance beween z=0 and z=1 covers the
    full possible operating hight
    '''
    def __init__(self, state, hardware_config):
        
        self.state = state
        self.hardware_config = hardware_config
        
        self.touchdown_localizer = TouchdownLocalizer(self.state)
        self.swing_controller = SwingController(self.touchdown_localizer)
        self.support_controller = SupportController(self.touchdown_localizer)
        self.stabilizer = Stabilizer(self.state)
        
        self.last_cycle  =    0.0
        self.last_update =    0.0
        
    def get_position(self):
        '''
        returns absolute leg coordinates in a 4x3 array
        if no update is needed, None is returned
        '''
        leg_state, leg_time = self.get_timing()
        if leg_state is not None:
            normalized_position = self.get_norm_position(leg_state, leg_time)
            abs_position = self.norm2abs_position(normalized_position)
            abs_position += self.correct_shoulder_displacement()
            abs_position = self.stabilizer.stabilize_gait(leg_state, leg_time, 
                                                          abs_position)
            self.state.absolute_foot_position = abs_position
        else:
            abs_position = None
        return abs_position
        
    def current_time(self):
        '''return current system time in ms'''
        return int(round(time.time() * 1000))
    
    def get_timing(self):
        '''
            manages the timing for the robots leg movement
        Returns:
            leg_state: 1x4 bool with leg states. 1 = supporting, 0 = swinging
            leg_time: 1x4 array with normalized times [0, 1] for each leg
        '''
        now = self.current_time()
        if (now - self.last_update) > self.state.update_time:
            self.state.true_update_time = now - self.last_update
            self.last_update = now
            if (now - self.last_cycle) > self.state.cycle_time:
                self.last_cycle = now
            t_norm = (self.state.phase
                      + (now - self.last_cycle) / self.state.cycle_time)
            t_norm %= 1
            leg_state = (t_norm <= self.state.support_ratio)
            leg_state = leg_state.astype(bool)
            # time for supporting legs
            leg_time = leg_state*t_norm/self.state.support_ratio
            # time for swinging legs
            leg_time += ~leg_state*((t_norm - self.state.support_ratio)
                                   /(   1.0 - self.state.support_ratio))
            self.state.leg_state = leg_state
            self.state.leg_time = leg_time
        else:
            # if no update is neccessary, signalize this by returning None
            leg_state = None
            leg_time = None
        return leg_state, leg_time
            
    
    def get_norm_position(self, leg_state, leg_time):
        '''
        Args:
            leg_state: 1x4 bool with leg states. 1 = supporting, 0 = swinging
            leg_time: 1x4 array with normalized times [0, 1] for each leg
        Returns:
            3x4 np.array with normalized leg coordinates
        '''
        position = ( self.swing_controller.get_position(leg_state,
                                                        leg_time) 
                   + self.support_controller.get_position(leg_state,
                                                          leg_time))
        self.state.normalized_foot_position = position
        return position
        
        
    def norm2abs_position(self, normalized_position):
        '''maps normalized to absolute coordinates, uses 3x4 np.arrays'''
        stride = self.state.velocity * self.state.cycle_time
        # add information for movement in z direction
        stride3 = np.append(stride, 2*self.hardware_config.leg_length)
        
        return (normalized_position * stride3[:, None])
    
    def correct_shoulder_displacement(self):
        '''
        Returns needed translation in y directionfor every foot position. 
        Foottips will be placed right under coxa or femur joint of inbetween
        (based on correct_shoulder_displacement, which is between 1 and 0)
        '''
        pos = np.zeros((3,4))
        pos[1] = ( self.hardware_config.shoulder_displacement
                 * np.abs(np.sign(self.hardware_config.leg_locations[1]))
                 * self.state.correct_shoulder_displacement)
        return pos
        
        
        
        