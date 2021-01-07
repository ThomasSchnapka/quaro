# -*- coding: utf-8 -*-
"""

[1]---------------[3]
 |                 |
 |                 |
 |    <--(x) Z     |    
 |    X   |        |
 |        V  Y     |
[0]---------------[2]

(coordinate origin is geometric center )
"""

import numpy as np


class HardwareConfig:
    def __init__(self):
        
        self.leg_length = 80 # assuming both legs have the same length
        self.shoulder_displacement = 45 # y-distance femur coxa joint in
        
        
        self.leg_locations = np.array([10.0*np.array([ 1, 1, -1, -1]),
                                        6.0*np.array([ 1,-1,  1, -1]),
                                            np.array([ 0, 0,  0,  0])])
        
        # serial data
        self.serial_baudrate = 115200
        self.serial_timeout = 3
        # To-Do: add all hardware details
        
    def inverse_kinematics(self, coordinates):
        '''
        Argument: coordinates for each leg, 3x4 np.array
        Returns: angles for each leg, 3x4 np.array
                 [[femur], [tibia], [coxa]]
        '''
        l = np.sqrt(     coordinates[1]**2
                    +    coordinates[2]**2
                    + self.shoulder_displacement**2)
        
        g = np.sqrt(     coordinates[0]**2
                    +    coordinates[1]**2
                    +    coordinates[2]**2
                    + self.shoulder_displacement**2)
        
        femur = (  np.arcsin(coordinates[0]/g)
                 + np.arccos(g / (2*self.leg_length)))
        tibia = 2.0*np.arccos(g / (2*self.leg_length))
        '''
        coxa = np.arccos((coordinates[2]+(self.shoulder_displacement
                          *coordinates[1])/l)
                         /((self.shoulder_displacement**2)/l + l))
        '''
        coxa = ((np.pi/2) - np.arctan(coordinates[1]/coordinates[2])
                - np.arctan(l/self.shoulder_displacement))
        angles = np.array([femur, tibia, coxa])
        # convert to deg
        angles *= 360.0/(2.0*np.pi)
        return angles