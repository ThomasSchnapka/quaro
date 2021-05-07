import numpy as np
import time

from src.Stabilizer import Stabilizer
from src.COMTrajectory import COMTrajectory
from src.LegTrajectory import LegTrajectory


class GaitController:
    '''
    Decides wether leg is swinging or supporting, calculates their normalized
    coordinates and maps them to absolute ones
    
    Info regarding normalized leg positions: the z-position is considered 1 if 
    all angles are zero (leg is fully streched out). z-position of the shoulder
    joint is 0, which means that the distance beween z=0 and z=1 covers the
    full possible operating hight
    '''
    def __init__(self, state, hardware_config, contact_sensor):
        
        self.state = state
        self.hardware_config = hardware_config
        self.contact_sensor = contact_sensor
        
        self.stabilizer = Stabilizer(self.state, self.hardware_config)
        self.comtraj = COMTrajectory(state)
        self.leg_trajectory = LegTrajectory(state, self.comtraj, contact_sensor)
        
        self.update_time = state.update_time
        self.last_cycle  = time.time()
        self.last_update = time.time()
        self.system_start_time = time.time()
        
    def get_position(self, initial=False):
        '''
        returns absolute leg coordinates in a 4x3 array
        if no update is needed, None is returned
        
        Args:
            initial: bool, if set to true returns initial leg position
        '''
        t = self.get_time()
        if t is not None:
            self.comtraj.update_state(t)
            if t%4 > 0.47 and t%4 < 0.6:
                self.contact_sensor.leg_state = np.ones(4).astype(bool)
                print("[GaitController] contact")
            else:
                self.contact_sensor.leg_state = np.zeros(4).astype(bool)
            pos = self.leg_trajectory.get_leg_position(t)
            print(pos[2,:])
            return pos
        else:
            return None
    
    
    def get_time(self):
        '''
        returns time in s since system was started
        '''
        now = time.time()
        if (now - self.last_update) > self.update_time:
            return (now - self.system_start_time)
        else:
            return None
        
        
        
        