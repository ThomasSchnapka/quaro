from src.utils.PID import PID
import numpy as np

class InclinationController:
    '''
    TODO
    '''
    
    
    def __init__(self, state, hardware_interface, hardware_config):
        
        # robot controller instances
        self.state = state
        self.hardware_interface = hardware_interface
        self.hardware_config = hardware_config
        
        # PID values
        self.kp = self.state.inc_kp
        self.ki = self.state.inc_ki
        self.kd = self.state.inc_kd
        self.setpoint = self.state.inc_setpoint
        self.pid = PID(self.kp, self.ki, self.kd, self.setpoint)
        
        # maximum values
        self.max_inc_x = 10
        self.max_inc_y = 10
        
    def correct_inclination(self, coordinates):
        '''
        

        Parameters
        ----------
        coordinates : TYPE
            DESCRIPTION.

        Returns
        -------
        (3,4) numpy.ndarray with corrected coordinates

        '''
        coordinates = np.copy(coordinates)
        
        inc_x, inc_y = self.hardware_interface.gyro.get_inclination()
        print(inc_x, inc_y)
        
        inc_x = 10
        inc_y = 0
        
        # check for extreme values
        inc_x = np.min([np.abs(inc_x), self.max_inc_x])*np.sign(inc_x)
        inc_y = np.min([np.abs(inc_y), self.max_inc_y])*np.sign(inc_y)
        
        # create array in a readable form for rot_rpy()
        inclination_angles = np.array([0, inc_y, inc_x])
        
        ## rotate coordinates around projection of com onto ground
        
        # convert coordinates into transformable form
        coordinates = np.vstack((coordinates, np.ones(4)))
        leg_location = np.vstack((self.hardware_config.leg_location, np.ones(4)))
        rotation_location = np.ones((4,4))
        rotation_location[:, :2] *= 0
        rotation_location[:, 2] *= (self.state.operating_hight
                                     *(    self.hardware_config.l1
                                         + self.hardware_config.l2))
        rotation_location = rotation_location.T
        
        # transform coordinates into body coordinate system
        foot_tips = coordinates + leg_location + rotation_location
        
        # rotate coordinates in body coordinate system
        foot_tips = self.hardware_config.rot_rpy(inclination_angles)@foot_tips
        
        # transform back to shoulder coordinate system
        foot_tips = foot_tips - leg_location - rotation_location
        
        # remove trailing ones
        coordinates = foot_tips[:3, :]
        
        return coordinates
        