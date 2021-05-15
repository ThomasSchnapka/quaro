#import numpy as np
import time

#from src.Stabilizer import Stabilizer
from src.cpp.GaitController_py import GaitController_py


class GaitController:
    '''
    Decides wether leg is swinging or supporting, calculates their normalized
    coordinates and maps them to absolute ones
    
    Info regarding normalized leg positions: the z-position is considered 1 if 
    all angles are zero (leg is fully streched out). z-position of the shoulder
    joint is 0, which means that the distance beween z=0 and z=1 covers the
    full possible operating hight
    '''
    def __init__(self, state):
        
        self.state = state
        
        self.update_time = state.update_time
        self.last_cycle  = 0
        self.last_update = 0
        self.t_init = time.time()
        
        #self.stabilizer = Stabilizer(self.state)
        #self.comtraj = COMTrajectory(self.state, self.stabilizer)
        self.gc = GaitController_py()
        self.gc.set_vel_x(0.0)
        self.gc.set_support_ratio(0.8)
        self.gc.set_cycle_time(2)
        self.gc.set_swing_hight(0.015)
        
    def get_position(self, initial=False):
        '''
        returns absolute leg coordinates in a 4x3 array
        if no update is needed, None is returned
        
        Args:
            initial: bool, if set to true returns initial leg position
        '''
        t = self.get_time()
        if t is not None:
            pos = self.gc.get_leg_position(t)
            #pos = self.rotation_controller.rotate(abs_position,
            #                                      leg_state, leg_time)
            pos[2,:] = self.state.operating_hight - pos[2,:]
            return pos
        else:
            return None
    
    
    def get_time(self):
        '''
        returns time in s since system was started
        '''
        now = time.time() - self.t_init
        if (now - self.last_update) > self.update_time:
            self.state.true_update_time = (now - self.last_update)
            self.last_update = now
            return now
        else:
            return None
        
        
        
        