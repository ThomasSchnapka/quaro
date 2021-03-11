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
from . import calibration
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
        
        
        self.leg_location = np.array([self.a*0.5*np.array([ 1, 1, -1, -1]),
                                      self.b*0.5*np.array([-1, 1, -1,  1]),
                                                 np.array([ 0, 0,  0,  0])])
        
        self.zero_pos = calibration.load_zero_pos()
        
        # I2C-PWM-board settings
        self.i2c_address = 0x40
        self.servo_pwm_min = 500
        self.servo_pwm_max = 2500
        self.servo_pwm_freq = 50
        self.servo_angle_range = 120
        self.servo_channels = np.array([[0, 4, 8, 12],  # femur
                                        [1, 5, 9, 13],  # coxa
                                        [2, 6,10, 14]]) # tibia
        
    def translate(self, coordinates):
        return np.array([[1, 0, 0, coordinates[0]],
                         [0, 1, 0, coordinates[1]],
                         [0, 0, 1, coordinates[2]],
                         [0, 0, 0,              1]])
    
    def rot_z(self, angle):
        # conversion to RAD
        angle = np.copy(angle*2*pi/360)
        return np.array([[cos(angle), -sin(angle),           0,           0],
                         [sin(angle),  cos(angle),           0,           0],
                         [         0,           0,           1,           0],
                         [         0,           0,           0,           1]])
    
    def rot_x(self, angle):
        # conversion to RAD
        angle = np.copy(angle*2*pi/360)
        return np.array([[         1,           0,           0,           0],
                         [         0,  cos(angle), -sin(angle),           0],
                         [         0,  sin(angle),  cos(angle),           0],
                         [         0,            0,          0,           1]])
    
    def rot_y(self, angle):
        # conversion to RAD
        angle = np.copy(angle*2*pi/360)
        return np.array([[ cos(angle),            0,  sin(angle),           0],
                         [          0,            1,           0,           0],
                         [-sin(angle),            0,  cos(angle),           0],
                         [          0,            0,           0,           1]])
    
    
    def rot_rpy(self, rpy):
        return self.rot_z(rpy[0])@self.rot_y(rpy[1])@self.rot_x(rpy[2])
    
    
    def inverse_kinematics(self, coordinates, rpy=np.zeros(3), 
                           rotation_center=np.zeros(3)):
        '''
        Vectorised inverse kinematics

        Parameters
        ----------
        coordinates : (3,4) numpy.ndarray, absolute coordinates for each leg
        rpy : 3 numpy.ndarray, roll, pitch and yaw in DEG
        rotation_center : 3 numpy.ndarray, axis the rotations are done around

        Returns
        -------
        angles : (3,4) numpy.ndarray
                 angles for each leg in DEG [[femur], [tibia], [coxa]]

        '''
        # local copy of coordinates variable as Python is pass by reference
        coordinates = np.copy(coordinates)
        
        ## influence of pitch, roll, yaw
        
        # convert coordinates into transformable form
        coordinates = np.vstack((coordinates, np.ones(4)))
        leg_location = np.vstack((self.leg_location, np.ones(4)))
        rotation_location = np.ones((4,4))
        rotation_location[:, :3] *= rotation_center
        rotation_location = rotation_location.T
        
        # transform coordinates into body coordinate system
        foot_tips = coordinates + leg_location + rotation_location
        
        # rotate coordinates in body coordinate system
        foot_tips = self.rot_rpy(-rpy)@foot_tips
        
        # transform back to shoulder coordinate system
        foot_tips = foot_tips - leg_location - rotation_location
        
        
        x = foot_tips[0]
        y = foot_tips[1]
        z = foot_tips[2]
        
        
        # coordinate systems of leg 1 and 3 are rotated around z
        #x[[1,3]] *= -1
        y[[1,3]] *= -1
        
        # inverse kinematics calculation, definitions can be found in doc
        B = sqrt(y**2 + z**2)
        A = sqrt(B**2 - self.g**2)# - self.h
        gamma = arctan(-y/z) - arcsin(self.g/B)
        C = sqrt(A**2 + x**2)
        C1 = ( self.l1**2 - self.l2**2 + C**2)/(2*C)
        C2 = (-self.l1**2 + self.l2**2 + C**2)/(2*C)
        alpha1 = -arctan(-x/A)
        alpha2 = -arccos(C1/self.l1)
        teta = -arccos(C2/self.l2)
        alpha = alpha1 + alpha2
        beta = -(teta + alpha2)
        
        # coordinate systems of leg 1 and 3 are rotated around z
        alpha[[1,3]] *= -1
        beta[[1,3]] *= -1
        gamma[[1,3]] *= -1
        
        angles = np.array([alpha, beta, gamma])
        # convert to deg
        angles *= 360.0/(2.0*np.pi)
        
        # replace NaN with zero
        angles = np.nan_to_num(angles)
        
        return angles
    
    def zero_pos_menu(self, controller):
        calibration.zero_pos_menu(controller, self)