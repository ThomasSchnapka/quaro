"""
Contains data regarding robots current state
"""

import numpy as np
np.set_printoptions(precision=5)


class State:
    def __init__(self):
        
        # Robot gait
        self.support_ratio = 0.8
        #self.stability_ratio = 0.8
        #self.stability_amplitude = 0.015
        self.stability_amplitude = 0
        #self.phase = np.array([0.0, 0.25, 0.75, 0.5])  # walk
        self.phase = np.array([0.0, 0.5, 0.5, 0])       # trot
        self.true_com = np.array([-0.01, 0.0, 0.0])
        
        
        # Robot schedule
        #self.cycle_time       = 5.0   # walk
        self.cycle_time       = 2    # trot
        self.update_time      = 0.001
        self.true_update_time = 0.0
        
        # PID parameters for inclilation control
        self.inc_x_kp = 0.03#0.05
        self.inc_x_ki = 0#0.02#0.01
        self.inc_x_kd = -1e-3#-5e-5
        self.max_inc_x = 15#8
        self.inc_y_kp = 0.02#0.05#0.05
        self.inc_y_ki = 0#0.02#0.01
        self.inc_y_kd = -1e-3#-5e-5
        self.max_inc_y = 15#5
        self.inc_x, self.inc_y = 0, 0
        self.enable_inclination_controller = False
        
        
        # Robot states
        self.leg_state      = np.array([1, 1, 1, 1]).astype(bool) # supporting or not
        #self.last_leg_state = np.array([1, 1, 1, 1]).astype(bool)
        self.leg_time  = np.array([  0.0, 0.0, 0.0])
        self.x_com     = np.array([  0.0, 0.0, 0.0]) # COM position
        self.dx_com    = np.array([ 0.02, 0.0, 0.0]) # COM velocity   0.005
        self.rpy       = np.array([  0.0, 0.0, 0.0]) # COM rotation
        self.drpy      = np.array([  0.0, 0.0, 0.0]) # COM rotation velocity
        self.operating_hight = 0.22                  # operation z distance
        self.lay_down_hight = 0.85
        self.enable_transitions = False
        
        
        # Robot movement parameters
        #self.z_stride = 0.0       # maximal step height, currently unused
        self.correct_shoulder_displacement = 0.9 # 1 = foottip under C0/1
                                               # 0 = foottip under C4/5
        self.swing_hight = 0.025                # z-distance during swing
        #self.swing_hight_factor = 0.95
        
        # Robot location
        self.absolute_foot_position    = np.zeros((3, 4))
        self.uncorrected_foot_position = np.zeros((3, 4))
        self.joint_angle               = np.zeros((3, 4))
        
        # Debugging
        self.debug_communication = False # Force HI to print communication
        
        # Server
        self.enable_server_loop = False
    
        
    def debug(self):
        '''print all variables contained by this class, useful for debugging'''
        print("[State] debugging info")
        print("--------------------------------")
        variables = vars(self)
        for v in sorted(variables, key=len, reverse=True):
            print(v, '\t', str(variables[v]).replace('\n', ' '))
        print("--------------------------------")
        

