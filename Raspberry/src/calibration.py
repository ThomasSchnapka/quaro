'''
Additional menu in user interface for calibrating the servo angles
Controller sets all software angles to zero and user alters the servo angles
until the legs are in their initial position. Results get saved on Arduino
'''

def calibration_menu(controller, hardware_interface):
    print header
    controller.shun()
    joint = 't'
    leg = '0'
    joints = {'f':'0', 't':'1', 'c':'2'}
    amounts = {'+':'1', '-':'-1', '++':'10', '--':'-10'}
    while True:
        inp = raw_input("[calibration][" + joint + leg + "]-> ")
        if inp in ["n","q","quit"]:
            print "[calibration] Do you want to save the changes? y/n"
            while True:
                inp = raw_input("[calibration]-> ")
                if inp is "y":
                    hardware_interface.send("q")     # save values to EEPROM
                    print "[calibration] new zero positions saved!"
                    break
                elif inp in ["n","q","quit"]:
                    break
                else:
                    print "[calibration] There is no command: ",inp
            controller.shun()
            break
        elif inp in ['f', 't', 'c']:
            joint = inp
        elif inp in ['0', '1', '2', '3']:
            leg = inp
        elif inp in ["+", "-", "++", "--"]:
            hardware_interface.send("z:l" + leg + "j" + joints[joint]
                                    + "a" + amounts[inp])
        elif inp in ["h", "i"]:
            print instruction
        else:
            print "[calibration] There is no command: ", inp
    
    
# longer text files:

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