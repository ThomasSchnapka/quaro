"""
Mostly taken from:
http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/
"""
import time


class PID:
    def __init__(self, kp, ki, kd, setpoint=0):
        '''
        classical PID controller
        '''
        
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.err_sum = 0
        self.last_err = 0
        self.last_time = time.time()
        
        
    def compute(self, current_value):
        # How long since we last calculated
        now = time.time()
        time_change = now - self.last_time;
      
        # Compute all the working error variables
        error = (self.setpoint - current_value)
        self.err_sum += (error * time_change)
        d_err = (error - self.last_err) / time_change
      
        # Compute PID Output
        output_value = (  self.kp * error
                        + self.ki * self.err_sum
                        + self.kd * d_err)
      
        # Remember some variables for next time
        self.last_err = error;
        self.last_time = now;
        
        return output_value
        
# TEST -----------------------------------------------------------------------
       
import numpy as np
import matplotlib.pyplot as plt

N = 100
SETPOINT = 10
pid = PID(1, 0.1, 1e-4, SETPOINT)

x = np.zeros(N)

for n in range(1, N):
    x[n] = x[n-1] + pid.compute(x[n-1])
    time.sleep(0.02)
    
plt.plot(x)

