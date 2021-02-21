# -*- coding: utf-8 -*-
"""

[1]---------------[3]
 |        A  Y     |
 |        |        |
 |    <--(x) Z     |    
 |    X            |
 |                 |
[0]---------------[2]

(coordinate origin is geometric center )
"""

## imports and redefinitions
import numpy as np
# redefine some functions for better visualisation in code
sin = np.sin
cos = np.cos
tan = np.tan
sqrt = np.sqrt
pi = np.pi
arctan = np.arctan
arcsin = np.arcsin
arccos = np.arccos


class HardwareConfig:
    def __init__(self):
        
        ## Geometric definitions (in mm)
        self.a = 186     # body length
        self.b = 78      # body width
        self.h = 11      # vertical shoulder displacement
        self.g = 55      # horizontal shoulder displacement
        self.l1 = 108    # upper leg length
        self.l2 = 130    # lower leg length
        
        self.leg_length = 80 # assuming both legs have the same length
        self.shoulder_displacement = 45 # y-distance femur coxa joint in
        
        
        self.leg_location = np.array([self.a*np.array([ 1, 1, -1, -1]),
                                      self.b*np.array([-1, 1, -1,  1]),
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
        
    
    def rot_z(self, angle):
        return np.array([[cos(angle), -sin(angle),           0,           0],
                         [sin(angle),  cos(angle),           0,           0],
                         [         0,           0,           1,           0],
                         [         0,           0,           0,           1]])
    def rot_x(self, angle):
        
        return np.array([[         1,           0,           0,           0],
                         [         0,  cos(angle), -sin(angle),           0],
                         [         0,  sin(angle),  cos(angle),           0],
                         [         0,            0,          0,           1]])
    
    def rot_y(self, angle):
        return np.array([[ cos(angle),            0,  sin(angle),           0],
                         [          0,            1,           0,           0],
                         [-sin(angle),            0,  cos(angle),           0],
                         [          0,            0,           0,           1]])
    
    
    def rot_rpy(self, rpy_deg):
        # convert DEG to RAD
        rpy = (2*pi/360)*rpy_deg
        return self.rot_z(rpy[0])@self.rot_y(rpy[1])@self.rot_x(rpy[2])
    
    
    def inverse_kinematics(self, position, rpy=np.zeros(3)):
        '''
        Vectorised inverse kinematics
        
        TODO: implement IK of SpotMicro, values already given above

        Parameters
        ----------
        coordinates : (3,4) numpy.ndarray, absolute coordinates for each leg

        Returns
        -------
        angles : (3,4) numpy.ndarray
                 angles for each leg in DEG [[femur], [tibia], [coxa]]

        '''
        # create local copy position (because Python is pass by reference)
        coordinates = np.copy(position)
        
        # influence off pitch, roll and yaw on coordinates
        shoulder_coordinates = np.vstack((self.leg_location, np.ones(4)))
        T_rpy = self.rot_rpy(rpy)
        delta = shoulder_coordinates - T_rpy@shoulder_coordinates
        delta[:,[1,2]] *= -1    # rotated coordinate system
        coordinates -= delta[:3]
        
        L = sqrt(     coordinates[1]**2
                 +    coordinates[2]**2
                 + self.shoulder_displacement**2)
        
        G = sqrt(     coordinates[0]**2
                 +    coordinates[1]**2
                 +    coordinates[2]**2
                 + self.shoulder_displacement**2)
        
        femur = (     arcsin(coordinates[0]/G)
                 +    arccos(G / (2*self.l1)))
        tibia = 2.0*arccos(G / (2*self.l1))
        coxa = ((pi/2) - arctan(coordinates[1]/coordinates[2])
                - arctan(L/self.h))
        
        #invert coxa of leg 1 and 3
        coxa[np.array([False, True, False, True])] *= -1
        tibia[np.array([False, True, False, True])] *= -1
        femur[np.array([True, False, True, False])] *= -1
        
        angles = np.array([femur, tibia, coxa])
        # convert to deg
        angles *= 360.0/(2.0*np.pi)
        return angles