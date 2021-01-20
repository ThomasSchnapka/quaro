class UserInterface:
    def __init__(self, controller, state):
        self.controller = controller
        self.state = state
        
    def run(self):
        '''
        runs user interface in while-true-loop
        other programm parts need single threads
        '''
        print header
        try:
            while True:         
                inp = raw_input("[UserInterface]-> ")
                if inp in ["s","start","go"]:
                    self.controller.start_gait()
                elif inp in ["stop"]:
                    self.controller.stop_gait()
                elif inp == "shun":
                    self.controller.shun()
                elif inp in ["q","quit","exit"]:
                    print("[main] initalizing shutdown!")
                    self.controller.stop_gait()
                    break
                elif inp in ["c","calibrate"]:
                    self.controller.calibrate()
                elif inp in ["help", "h"]:
                    print "[help] No help available. Help has to be extended!"
                elif inp in ["debug", "d"]:
                    self.state.debug()
                elif inp in ["demo"]:
                    self.controller.start_demo()
                else:
                    print "[UserInterface] There is no command for '", inp, "'"
                '''
                elif inp == "send":
                    #"send messages directly via serial"
                    inp = raw_input("[Message without '<>']->")
                    communication.send_command(inp)
                elif inp in ["z", "zero", "zeropos"]:
                    zeropos_menu()
                '''
                    
        except KeyboardInterrupt:
            print "[main] end"
            
            
# longer texts:
            
header = "\n+------------------+\n"\
        +  "|    QUARO-MENU    |\n"\
        +  "+------------------+\n"\
        +  "[UI] waiting for commands. Type 'h' for help."
        
        