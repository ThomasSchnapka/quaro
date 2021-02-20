#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Module that manages the communication with external hardware. So far only
the I2C PWM boad has been implemented. Accelerometer and foot contact switched
will be added later

The PCA9685 library is quite old, thus we have to handle it somehow ... special

'''


import numpy as np

# conditional import to make this script runnable without connected hardware
try:
    from .Adafruit_Python_PCA9685.Adafruit_PCA9685 import PCA9685
    # PCA9685 module relys on the following one. This can only be used on
    # Raspberry Pi and therefore is tested in this try execpt block, too
    import Adafruit_GPIO.I2C as I2C
except OSError as err:
    print("[HardwareInterface] OS error: {0}. "\
          "Did you enable I2C in Raspberry config?".format(err))

except ModuleNotFoundError:
    print("[HardwareInterface] I2C PWM module not found. "\
          "Creating dummy module for tests")
    # dummy module
    class PCA9685:
        def __init__(self, address):
            pass
        
        def set_pwm_freq(self, f):
            pass
        
        def set_pwm(self, channel, on, pulse):
            pass

            
        

class HardwareInterface:

    def __init__(self, hardware_config, state):
        
        self.state = state
        self.hardware_config = hardware_config
        
        # I2C-PWM-board settings
        self.i2c_address = self.hardware_config.i2c_address
        self.servo_pwm_min = self.hardware_config.servo_pwm_min
        self.servo_pwm_max = self.hardware_config.servo_pwm_max
        self.servo_pwm_freq = self.hardware_config.servo_pwm_freq
        self.servo_angle_range = self.hardware_config.servo_angle_range #120deg
        self.servo_channels = self.hardware_config.servo_channels
        
        # initialize board
        self.pwm_board = PCA9685(address=self.i2c_address)
        self.pwm_board.set_pwm_freq(self.servo_pwm_freq)
            
    
            
    def set_servo_angle(self, angle):
        '''
        send angles to PCA9685 board
        
        PCA9685 library only accepts amount of bits instead of PWM duty ratios
        as one might expect. The pulse_bits variable represents the duty ratio
        mapped to 12 bits of period duration

        Parameters
        ----------
        angle : (3,4) numpy.ndarray with angles to be sent
                (as calculated by robot controller)

        '''
        # convert angles to pulse duration
        pulse_duration =  angle*((self.servo_pwm_max - self.servo_pwm_min)
                                 /(self.servo_angle_range))
        pulse_duration += (self.servo_pwm_min 
                           + (self.servo_pwm_max - self.servo_pwm_min)/2)
        
        # convert pulse duration to pulse bits
        period = 1e6/self.servo_pwm_freq                # in us
        pulse_bits = (2**12)*(pulse_duration/period)    # 12 bits
        for p, c in zip(pulse_bits.flatten(), self.servo_channels.flatten()):
            # PCA9685 performs bitwise operations, therefore conversion to int
            self.pwm_board.set_pwm(int(c), 0, int(p))
            #print("channel", c, "pulse", p)

        
    
    def send_angle(self, angle):
        '''
        sends servo angles to I2C PWM board

        Parameters
        ----------
        angle : (3,4) numpy.ndarray with angles to be sent
                (as calculated by robot controller)

        '''
        # ensure that angles are within rangee:
        angle[angle >  self.servo_angle_range/2] =  self.servo_angle_range/2
        angle[angle < -self.servo_angle_range/2] = -self.servo_angle_range/2
        if self.state.debug_communication:
            print("[HardwareInterface] sending angles:")
            print(angle)
        self.set_servo_angle(angle)
  

      
#---------------------------- standalone test -------------------------------#

if __name__ == "__main__":
    # module test    
    
    # class dummy
    class HardwareConfig:
        def __init__(self):
            # I2C-PWM-board settings
            self.i2c_address = 0x40
            self.servo_pwm_min = 500
            self.servo_pwm_max = 2500
            self.servo_pwm_freq = 50
            self.servo_angle_range = 120
            self.servo_channels = np.array([[0, 4, 8, 12],
                                            [1, 5, 9, 13],
                                            [2, 6,10, 14]])
    
    # class dummy
    class State:
        def __init__(self):
            self.debug_communication = True
    
    
    # create objects
    hc = HardwareConfig()
    state = State()      
    hi = HardwareInterface(hc, state)
    
    print("[HardwareInterface] standalone test run")
    
    angles = np.random.randint(-120, 120, (3,4))
    hi.send_angle(angles)
    