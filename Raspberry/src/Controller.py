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
        self.hardware_interface.send_angle(angle_shun)
        self.state.joint_angle = angle_shun
        pass
    
    def shutdown(self):
        # To-Do
        pass
    
    def gait_loop(self):
        while self.allow_loop:
            self.update_leg_position()
        
    def update_leg_position(self):
        '''updates leg positons if neccessary'''
        position = self.gait_controller.get_position()
        if position is not None:
            self.set_leg_position(position)
        else:
            # no update is needed
            pass
        
    def set_leg_position(self, position):
        '''
        calculates angles out of absolute cartesian leg positions 
        and sends them
        '''
        angle = self.hardware_config.inverse_kinematics(position)
        self.set_leg_angle(angle)
        
    def set_leg_angle(self, angle):
        '''check and save angles to hardware interface'''
        self.state.joint_angle = angle
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
        