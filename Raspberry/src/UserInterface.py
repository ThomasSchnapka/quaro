from .QuaroServerHandler import QuaroServerHandler

class UserInterface:
    def __init__(self, controller, state, hardware_config):
        self.controller = controller
        self.state = state
        self.hardware_config = hardware_config
        self.quaro_server_handler = QuaroServerHandler(self.state)
        
    def run(self):
        '''
        runs user interface in while-true-loop
        other programm parts need single threads
        '''
        print("[UserInterface] waiting for commands. Type 'h' for help.")
        try:
            while True:
                self.print_header()
                inp = input("[UserInterface]-> ")
                if inp in ["s","start","go"]:
                    self.controller.start_gait()
                elif inp in ["stop"]:
                    self.controller.stop_gait()
                elif inp == "shun":
                    self.controller.shun()
                elif inp in ["q","quit","exit"]:
                    print("[main] initalizing shutdown!")
                    self.controller.shutdown()
                    self.quaro_server_handler.stop()
                    break
                elif inp in ["c","calibrate"]:
                    self.controller.calibrate()
                elif inp in ["server"]:
                    self.quaro_server_handler.start()
                elif inp in ["stopserver"]:
                    self.quaro_server_handler.stop()
                elif inp in ["help", "h"]:
                    self.print_help()
                elif inp in ["debug", "d"]:
                    self.state.debug()
                elif inp in ["demo"]:
                    self.controller.stop_gait()
                    self.controller.start_demo()
                elif inp in ["raise", "raise up"]:
                    self.controller.stop_gait()
                    self.controller.raise_up()
                elif inp in ["lay", "lay down"]:
                    self.controller.stop_gait()
                    self.controller.lay_down()
                elif inp in ["twerk"]:
                    self.controller.stop_gait()
                    self.controller.start_demo("twerk")
                elif inp in ["z", "zero", "zeropos"]:
                    self.hardware_config.zero_pos_menu(self.controller)
                elif inp[:6] == "change":
                    self.change_parameter(inp[7:])
                else:
                    print("[UserInterface] There is no command for '", inp, "'")
        except KeyboardInterrupt:
            print("[main] end")
    
    
    def change_parameter(self, inp):
        '''
        function called by UI to change parameters. As there is an if-statement
        for each parameter, it is kinda messy. Here is an overview of possible
        commands/parameters. Please by aware that the parameters will be changed
        without any sanity check!

        support_ratio: sr
        velocity_x:    vx
        velocity_y:    vy
        cycle_time:    ct
        stab'_ratio:   str
        shoulder_dis:  sd
        op'_hight:     oh
        swing_h_fact': shf
        roll:          r
        pitch:         p
        yaw:           y
        true_com_x:    tcx
        true_com_y:    tcy

        '''
        space_char = inp.find(' ')
        if space_char != -1:
            parameter = inp[:space_char]
            value = inp[space_char+1:]
            if parameter in ["support_ratio", "sr", "spr"]:
                self.state.support_ratio = float(value)
            elif parameter in ["velocity_x", "vx"]:
                self.state.dx_com[0] = float(value)
            elif parameter in ["velocity_y", "vy"]:
                self.state.dx_com[1] = float(value)
            elif parameter in ["cycle_time", "ct"]:
                self.state.cycle_time = float(value)
            elif parameter in ["stability_ratio", "str"]:
                self.state.stability_ratio = float(value)
            elif parameter in ["stability_amplitude", "sa"]:
                self.state.stability_amplitude= float(value)
            elif parameter in ["shoulder_dis", "sd"]:
                self.state.correct_shoulder_displacement = float(value)
            elif parameter in ["operating_hight", "oh"]:
                self.state.operating_hight = float(value)
            elif parameter in ["swing_hight_factor", "shf"]:
                self.state.swing_hight_factor = float(value)
            elif parameter in ["roll", "r"]:
                self.state.rpy[0] = float(value)
            elif parameter in ["pitch", "p"]:
                self.state.rpy[1] = float(value)
            elif parameter in ["yaw", "y"]:
                self.state.rpy[2] = float(value)
            elif parameter in ["true_com_x", "tcx"]:
                self.state.true_com[0] = float(value)
            elif parameter in ["true_com_y", "tcy"]:
                self.state.true_com[1] = float(value)
            elif parameter in ["angular_velocity", "av"]:
                self.state.drpy[2] = float(value)
            else:
                print(f"[UserInterface] could not match {parameter}:{value}")
                print("Use 'h' to show available parameters")
        else:
            print("[UserInterface] invalid command: input ", inp)
            
            
    def print_header(self):
        '''Header for user interface containing parameters'''
        print("\n\n\n")
        print("==============================================================")
        print("\n+------------------+\n"\
              + "|    QUARO-MENU    |\n"\
              + "+------------------+\n")
        print("--------------------------------------------------------------")
        print(f"support_ratio: {self.state.support_ratio}".ljust(30),
              f"phase:         {self.state.phase}")
        print(f"cycle_time:    {self.state.cycle_time}".ljust(30),
              f"velocity:      {self.state.dx_com}")
        print(f"stab'_ratio:   ".ljust(30),
              f"rpy:           {self.state.rpy}")
        print(f"op'_hight:     {self.state.operating_hight}".ljust(30),
              f"true_com:      {self.state.true_com}")
        print(f"shoulder_dis': {self.state.correct_shoulder_displacement}".ljust(30),
              f"swing_h'_fact':")
        print(f"server_status':{self.state.enable_server_loop}".ljust(30),
              f"ang'_velocity':{self.state.drpy}")
        print(f"stab'_ampl':   {self.state.stability_amplitude}".ljust(30))
        print("--------------------------------------------------------------")
            

    def print_help(self):
         '''list of functions of UI'''
         print("[Help] Type in the commands as following:")
         print("  s/start:     start gait\n"\
               "  stop:        stop gait\n"\
               "  demo:        do roll pitch yaw demo\n"\
               "  server:      start server\n"\
               "  stopserver:  stop server\n"\
               "  d/debug:     show all parameters of state\n"\
               "  h/help:      show this help\n"\
               "  z/zeropos:   enter servo calibration mode\n"\
               "  q/quit       quit programm")
         print("  ------")
         print("  change [parameter] [value]   change parameters")
         print("  changable paramters are:\n"\
               "  support_ratio: srv\n"\
               "  velocity_x:    vx\n"\
               "  velocity_y:    vy\n"\
               "  cycle_time:    ctv\n"\
               "  stab'_ratio:   str\n"\
               "  stab'_ampl:    sa\n"\
               "  shoulder_dis:  sd\n"\
               "  op'_hight:     oh\n"\
               "  swing_h_fact': shf\n"\
               "  roll:          r\n"\
               "  pitch:         p\n"\
               "  yaw:           y\n"\
               "  true_com_x:    tcx\n"\
               "  true_com_y:    tcy\n"\
               "  angular_vel'': av\n")

        
        