'''
Gyro library

makes use of Adafruits MPU6050 module:
https://github.com/adafruit/Adafruit_CircuitPython_MPU6050
'''

import numpy as np

# conditional import to make this script runnable without connected hardware
try:
    import board
    import busio
    import adafruit_mpu6050
except OSError as err:
    print("[GyroInterface] OS error: {0}. "\
          "Did you enable I2C in Raspberry config?".format(err))
except ModuleNotFoundError:
    print("[GyroInterface] adafruit_mpu6050 module not found. "\
          "Creating dummy module for tests. Did you download the submodule?")
    # dummy module
    class GyroInterface:
        def __init__(self):
            pass
        
        def get_inclination(self):
            return 0, 0
else:
    class GyroInterface:
        def __init__(self):
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.mpu = adafruit_mpu6050.MPU6050(self.i2c)
        
            # settings for filtering if data becomes too noisy:
            # self.mpu.cycle_Rate = adafruit_mpu6050.Rate.CYCLE_5_HZ
            # self.mpu.filter_bandwidth = adafruit_mpu6050.Bandwidth.BAND_260_HZ
        
        
        def get_inclination(self):
            '''return inclination measured around x and y'''
            acc_x, acc_y, acc_z = self.mpu.acceleration
            inc_x = -np.arctan2(acc_y, acc_z) * 360/(2*np.pi)
            inc_y = -np.arctan2(acc_x, acc_z) * 360/(2*np.pi)
            return inc_x, inc_y


if __name__ == "__main__":
    import time
    gyro = GyroInterface()
    
    while True:
        angle_x, angle_y = gyro.get_inclination()
        print(f"inc_x: {angle_x:.3}     inc_y: {angle_y:.3}")
        time.sleep(0.2)
    
    