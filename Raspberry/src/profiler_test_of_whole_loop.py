from quaro.HardwareConfig import HardwareConfig

from src.HardwareInterface import HardwareInterface
from src.State import State
from src.Controller import Controller

import time

def main():
    # independend objects
    hardware_config = HardwareConfig()
    state = State()
    hardware_interface = HardwareInterface(hardware_config, state)
    
    # dependend objects
    controller = Controller(hardware_config,
                            state,
                            hardware_interface)
    controller.start_gait()
    
    time.sleep(10)
    
    # shutdown procedure:
    controller.shutdown()
    
main()