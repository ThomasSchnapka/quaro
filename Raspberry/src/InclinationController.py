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
        self.setpoint_x = 0
        self.setpoint_y = 0
        self.pid_x = PID(self.kp, self.ki, self.kd, self.setpoint_x)
        self.pid_y = PID(self.kp, self.ki, self.kd, self.setpoint_y)
        
        # maximum values
        self.max_inc_x = self.state.max_inc_x
        self.max_inc_y = self.state.max_inc_y
        
        # saved values
        self.last_inc_x = 0
        self.last_inc_y = 0
        
        # transformation functions
        self.rot_x = self.hardware_config.rot_x
        self.rot_y = self.hardware_config.rot_y
        
        
    def correct_inclination(self, coordinates):
        '''
        
        ROTATION AROUND PROJECTION OF TRUE COM ON GROUND
        INPUT SHOULD ALREADY BE TRUE COM CORRECTED
        Parameters
        ----------
        coordinates : TYPE
            DESCRIPTION.

        Returns
        -------
        (3,4) numpy.ndarray with corrected coordinates

        '''
        coordinates = np.copy(coordinates)
        
        measured_inc_x, measured_inc_y = self.hardware_interface.gyro.get_inclination()
        
        #inc_x = self.last_inc_x + self.pid_x.compute(measured_inc_x)
        #inc_y = self.last_inc_y + self.pid_y.compute(measured_inc_y)
        inc_x = self.pid_x.compute(measured_inc_x)
        inc_y = self.pid_y.compute(measured_inc_y)
        
        
        # limit extreme values
        inc_x = np.min([np.abs(inc_x), self.max_inc_x])*np.sign(inc_x)
        inc_y = np.min([np.abs(inc_y), self.max_inc_y])*np.sign(inc_y)
        
        # save current counteract inclination
        self.last_inc_x = inc_x
        self.last_inc_y = inc_y
        
        # log (limited) inclination in state
        self.state.inc_x = inc_x
        self.state.inc_y = inc_y
        
        
        ## rotate coordinates around projection of com onto ground
        
        # convert coordinates into transformable form
        # foot_tips = coordinates + self.hardware_config.leg_location
        # foot_tips = np.vstack((foot_tips, np.ones(4)))
        #print("-------------")
        #print("before", coordinates)
        foot_tips = coordinates + self.hardware_config.leg_location
        # add row of ones for transformation
        foot_tips = np.vstack((foot_tips, np.ones(4)))
        #print("foot_tips", foot_tips)
        
        # translation to projected COM
        projected_com = np.copy(self.state.true_com)
        projected_com[2] = (self.state.operating_hight
                                     *(    self.hardware_config.l1
                                         + self.hardware_config.l2))
        foot_tips = self.hardware_config.translate(-projected_com)@foot_tips
        
        #print("projection", foot_tips)
        # rotate coordinates against inclination
        foot_tips = self.rot_x(inc_x)@self.rot_y(inc_y)@foot_tips
        #print("rot projection", foot_tips)
        
        # translate back to main body coordinate system
        foot_tips = self.hardware_config.translate(+projected_com)@foot_tips
        
        # remove trailing ones
        foot_tips = foot_tips[:3, :]
        
        # subtract leg_pos to get coordinates in leg frame
        coordinates = foot_tips - self.hardware_config.leg_location
        
        #print("after", coordinates)
        
        
        return coordinates
        