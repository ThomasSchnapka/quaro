"""
Contains data regarding robots current state
"""

import numpy as np
np.set_printoptions(precision=5)


class State:
    def __init__(self):
        
        # Robot gait
        self.support_ratio = 0.85
        self.stability_ratio = 0.5
        self.stability_amplitude = 15
        #self.phase = np.array([0.0, 0.25, 0.75, 0.5])  # walk
        self.phase = np.array([0.0, 0.5, 0.5, 0])       # trot
        self.true_com = np.array([-28, 0, 0])
        
        
        # Robot schedule
        #self.cycle_time       = 3000.0   # walk
        self.cycle_time       = 1500.0    # trot
        self.update_time      = 20.0
        self.true_update_time = 0.0
        
        
        # Robot states
        self.leg_state      = np.array([1, 1, 1, 1]).astype(bool) # supporting or not
        self.last_leg_state = np.array([1, 1, 1, 1]).astype(bool)
        self.leg_time  = np.array([0, 0, 0, 0])
        self.velocity  = np.array([0.00, 0.00])    # x and y direction, in m/s
        self.angular_velocity = 0.0                # rotation around z-axis in DEG/s
        self.rpy       = np.array([0.0, 0.0, 0.0]) # roll, pitch, yaw of body
        self.operating_hight = 0.95                # operation z distance
        self.lay_down_hight = 0.80
        
        
        # Robot movement parameters
        self.z_stride = 0.0       # maximal step height, currently unused
        self.correct_shoulder_displacement = 1 # 1 = foottip under C0/1
                                               # 0 = foottip under C4/5
        self.swing_hight_factor = 0.95
        
        # Robot location
        self.absolute_foot_position   = np.array([[  0,   0,   0,   0],
                                                  [-55,  55, -55,  55],
                                                  [200, 200, 200, 200]])
        self.uncorrected_foot_position   = np.array([[  0,   0,   0,   0],
                                                     [  0,   0,   0,   0],
                                                     [200, 200, 200, 200]])
        self.normalized_foot_position = np.zeros((3, 4))
        self.joint_angle              = np.zeros((3, 4))
        self.last_touchdown_point = np.array([[-0.5, -0.5, -0.5, -0.5],
                                              [-0.5, -0.5, -0.5, -0.5],
                                              self.operating_hight*np.ones(4)])
        self.next_touchdown_point = np.array([[0.5, 0.5, 0.5, 0.5],
                                              [0.5, 0.5, 0.5, 0.5],
                                              self.operating_hight*np.ones(4)])
    
        # Debugging
        self.debug_communication = False # Force HI to print communication
        
        # Server
        self.allow_server_loop = False
    
        
    def debug(self):
        '''print all variables contained by this class, useful for debugging'''
        print("[State] debugging info")
        print("--------------------------------")
        variables = vars(self)
        for v in sorted(variables, key=len, reverse=True):
            print(v, '\t', str(variables[v]).replace('\n', ' '))
        print("--------------------------------")
        

