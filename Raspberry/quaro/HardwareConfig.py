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
        
        # I2C-PWM-board settings
        self.i2c_address = 0x40
        self.servo_pwm_min = 500
        self.servo_pwm_max = 2500
        self.servo_pwm_freq = 50
        self.servo_angle_range = 120
        self.servo_channels = np.array([[0, 4, 8, 12],  # femur
                                        [1, 5, 9, 13],  # coxa
                                        [2, 6,10, 14]]) # tibia
        
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
        
        #invert coxa of leg 1 and 3a
        coxa[np.array([False, True, False, True])] *= -1
        tibia[np.array([False, True, False, True])] *= -1
        femur[np.array([True, False, True, False])] *= -1
        
        angles = np.array([femur, tibia, coxa])
        # convert to deg
        angles *= 360.0/(2.0*np.pi)
        return angles