"""
This module contains calibration functions. Currently, only functions
regarding the legs zero positions is implemented. To find the right zero
positions, type "zero" into the main gui and follow the instructions.

More information and the defintion of the zero positions can be found in docs
"""

import numpy as np

FILENAME = "quaro/zero_pos.csv"

def load_zero_pos():
    '''loads zero positions from file if available. Otherwise returns zero'''
    try:
        f = np.fromfile(FILENAME, sep=";")
        f = f.reshape((3,4))
    except FileNotFoundError:
        f = np.zeros((3,4))
        f.tofile(FILENAME, sep=";")
    return f

def save_zero_pos(zero_pos):
    '''save given zero positions to file'''
    if not zero_pos.shape == (3,4):
        print("[calibration] wrong shape of zero_pos:", zero_pos.shape)
        raise ValueError
    else:
        zero_pos.tofile(FILENAME, sep=";")

def zero_pos_menu(controller, hardware_config):
    '''
    Menu that guides user through calibration of the legs zero position
    See docs for how zero position is defined

    Parameters
    ----------
    controller : current controller instance
    hardware_config : current hardware_config instance


    '''
    print(header)
    controller.shun()
    joint = 't'
    leg = '0'
    joints = {'f':0, 't':1, 'c':2}
    amounts = {'+':1, '-':-1, '++':10, '--':-10}
    zero_pos = hardware_config.zero_pos
    while True:
        inp = input("[calibration][" + joint + leg + "]-> ")
        if inp in ["n","q","quit"]:
            print("[calibration] Do you want to save the changes? y/n")
            while True:
                inp = input("[calibration]-> ")
                if inp == "y":
                    save_zero_pos(zero_pos)
                    hardware_config.zero_pos = zero_pos
                    print("[calibration] new zero positions saved!")
                    break
                elif inp in ["n","q","quit"]:
                    hardware_config.zero_pos = load_zero_pos()
                    break
                else:
                    print("[calibration] There is no command: ",inp)
            controller.shun()
            break
        elif inp in ['f', 't', 'c']:
            joint = inp
        elif inp in ['0', '1', '2', '3']:
            leg = inp
        elif inp in ["+", "-", "++", "--"]:
            zero_pos[int(leg), joints[joint]] += amounts[inp]
            print(zero_pos)
            controller.shun()
        elif inp in ["h", "i"]:
            print(instruction)
        else:
            print("[calibration] There is no command: ", inp)
    
    
# longer texts:

header = "\n+------------------+\n"\
        +"|   ZEROPOS-MENU   |\n"\
        +"+------------------+\n"\
        +"Change the zero position of each joint\n"\
        +"Exit the menu:\t\tquit\n"\
        +"Choose the joint:\tf/t/c\n"\
        +"Choose the leg:\t\t0/1/2/3\n"\
        +"In/decrase zeroPos:\t+/-/++/--\n"\
        +"Send 'h' for help"
        
instruction =  "To be added."\
             + "Until then: just try it out, you can't break anyting"