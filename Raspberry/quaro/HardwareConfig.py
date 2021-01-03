"""

[1]---------------[3]
 |        Ʌ  Y     |
 |        |        |
 |    <--(x) Z     |    
 |    X            |
 |                 |
[0]---------------[2]

(coordinate origin is geometric center )
"""

import numpy as np


class HardwareConfig:
    def __init__(self):
        
        self.leg_length = 80 # assuming both legs have the same length
        
        
        self.leg_locations = np.array([10.0*np.array([ 1, 1, -1, -1]),
                                        6.0*np.array([-1, 1, -1,  1]),
                                            np.array([ 0, 0,  0,  0])])
        
        # serial data
        self.serial_baudrate = 115200,
        self.serial_timeout = 3
        # To-Do: add all hardware details
        
    def inverse_kinematics(self, coordinates):
        '''
        Argument: coordinates for each leg, 3x4 np.array
        Returns: angles for each leg, 3x4 np.array
                 [[femur], [tibia], [coxa]]
        '''
        l = np.linalg.norm(coordinates, axis=0)
        femur = (  np.arcsin(coordinates[0]/l)
                 + np.arccos(l / (2*self.leg_length)))
        tibia = 2.0*femur
        coxa = np.arcsin(coordinates[1]/l)
        angles = np.array([femur, tibia, coxa])
        # convert to deg
        angles *= 360.0/(2.0*np.pi)
        return angles