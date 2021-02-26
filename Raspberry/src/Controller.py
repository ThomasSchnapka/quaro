import threading
import numpy as np

from .GaitController import GaitController
from . import calibration
from . import demo


class Controller:
    '''
    Manages timing, calculates coordinates with gait_controller
    and sends them to hardware_interface
    
    To-Do: - implement IMU
           - implement control-loop with pressure sensors
    '''
    
    
    def __init__(self, hardware_config, state, hardware_interface):
        
        self.state = state
        self.hardware_interface = hardware_interface
        self.hardware_config = hardware_config
        
        self.gait_controller = GaitController(state, hardware_config)
        
        self.allow_loop = False
        
    def start_gait(self):
        # start thread
        self.allow_loop = True
        self.gait_loop_thread = threading.Thread(target=self.gait_loop,)
        self.gait_loop_thread.start()
        
    def stop_gait(self):
        self.allow_loop = False
        
    def shun(self):
        self.stop_gait();
        angle_shun = np.zeros((3, 4))
        self.set_leg_angle(angle_shun)
        self.state.joint_angle = angle_shun
        pass
    
    def shutdown(self):
        # To-Do
        pass
    
    def gait_loop(self):
        while self.allow_loop:
            self.check_for_position_updates()
        
    def check_for_position_updates(self):
        '''
        checks if it is time to update the leg position and updates is
        use this function in gait generation only!
        '''
        position = self.gait_controller.get_position()
        if position is not None:
            self.set_leg_position(position)
        else:
            # no update is needed
            pass
        
    def set_leg_position(self, coordinates, rpy=np.zeros(3)):
        '''
        calculates angles out of absolute cartesian leg positions 
        and sends them
        '''
        coordinates = np.copy(coordinates)
        coordinates += self.correct_shoulder_displacement()
        angle = self.hardware_config.inverse_kinematics(coordinates, rpy)
        # save values in state
        self.state.joint_angle = angle
        self.state.rpy = rpy
        self.set_leg_angle(angle)
        
    def set_leg_angle(self, angle):
        '''check and save angles to hardware interface'''
        angle += self.hardware_config.zero_pos
        self.sanity_check_angle(angle)
        self.hardware_interface.send_angle(angle)
        
    def sanity_check_angle(self, angle):
        '''check if angles can be used without flaws'''
        # TODO: add direct kinematics for a better verification
        if (    np.any(np.abs(angle[0]) > 60)
            or  np.any(np.abs(angle[1]) > 120)
            or  np.any(np.abs(angle[2]) > 60)
            or  np.any(np.isnan(angle))):
            self.state.debug()
            print("[controller] bad angle value")
            print(angle)
            raise Exception("[controller] unreachable angle detected!")
    
    def calibrate(self):
        calibration.calibration_menu(self, self.hardware_interface);
        
    def start_demo(self):
        demo.start_demo(self);
        
    def correct_shoulder_displacement(self):
        '''
        Returns needed translation in y directionfor every foot position. 
        Foottips will be placed right under coxa or femur joint of inbetween
        (based on correct_shoulder_displacement, which is between 1 and 0)
        '''
        pos = np.zeros((3,4))
        pos[1] = ( self.hardware_config.g
                 * np.sign(self.hardware_config.leg_location[1])
                 * self.state.correct_shoulder_displacement)
        return pos
        