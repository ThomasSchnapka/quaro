from quaro.HardwareConfig import HardwareConfig

from src.HardwareInterface import HardwareInterface
from src.State import State
from src.Controller import Controller
from src.UserInterface import UserInterface

# To-Do: import threading


def main():
    # independend objects
    hardware_config = HardwareConfig()
    state = State()
    hardware_interface = HardwareInterface(hardware_config, state)
    
    # dependend objects
    controller = Controller(hardware_config,
                            state,
                            hardware_interface)
    user_interface = UserInterface(controller, state)
    
    # calling UI, which handles the whole robot control
    
    user_interface.run()
    
    # user interface runs in loop, if closed the whole programm has to stop
    # shutdown procedure:
    hardware_interface.shutdown()
    controller.shutdown()
    
main()



    