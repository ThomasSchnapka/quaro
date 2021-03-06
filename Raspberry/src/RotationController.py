import numpy as np

class RotationController:
    '''controls rotatory movement around z-axis'''
    
    def __init__(self, state, hardware_config):
        
        self.state = state
        self.hardware_config = hardware_config
        
        
    def rotate(self, abs_position, leg_state, leg_time):
        '''
        Returns the change of coordinates for rotation. This works similar
        to roll, pitch, yaw with the difference that a continuous rotation
        is possible because the legs swing to a new position
        
        Args:
            abs_position: 3x4 np.ndarray with absolute, unrotated leg coordnates
            leg_state: 1x4 bool with leg states. 1 = supporting, 0 = swinging
            leg_time: 1x4 array with normalized times [0, 1] for each leg
        Returns:
            3x4 np.array with rotated leg coordinates
        '''
        
        
        coordinates = np.copy(abs_position)
        
        # convert coordinates into transformable form
        coordinates = np.vstack((coordinates, np.ones(4)))
        leg_location = np.vstack((self.hardware_config.leg_location, np.ones(4)))
        
        # transform coordinates into body coordinate system
        coordinates = coordinates + leg_location
        
        angles = np.copy(leg_time)
        angles[~leg_state] = 1-angles[~leg_state]
        angles -= 0.5
        angles *= self.state.angular_velocity
        angles *= 2*np.pi/360
        # rotiation per leg, no clue how to vectorize this
        for n in range(4):
            coordinates[:,n] = self.hardware_config.rot_z(angles[n])@coordinates[:,n]
            
        # transform back to shoulder coordinate system
        coordinates -= leg_location
        #print("[RotationController]", coordinates)
        return coordinates[:3]