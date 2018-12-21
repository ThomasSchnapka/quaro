'''
Manages threads, server and builds up the shell menu.
'''

__version__ = '1.1'
__author__ = 'Thomas Schnapka'


import threading
import quaroShared as sh
import quaroMotion as motion


def change_value(name, val=None):
    '''
    Changes the value of variables stored in sh.Data.
    This if-else-list is ugly but necessary because there are no pointers
    in Python.
    '''
    
    def print_info(name, val):
        print "set " + str(name) + " to " + str(val)
            
    if val is not None:
        val = float(val)
    if name is "stride":
        sh.Data.stride_x = val
        print_info(sh.Data.stride_x)
    elif name is "rotation":
        sh.Data.teta = val/1000.0
        print_info(name, sh.Data.teta)
    elif name is "supp":
        sh.Data.supportRatio = val
        print_info(name, sh.Data.supportRatio)
    elif name is "comx":
        sh.Data.com_adjust[0] = val
        print_info(name, sh.Data.com_adjust[0])
    elif name is "comy":
        sh.Data.com_adjust[1] = val
        print_info(name, sh.Data.teta)
    elif name is "distr":
        sh.Data.distribution = val
        print_info(name, sh.Data.distribution)
    elif name is "hight":
        sh.Data.hight = val
        print_info(name, sh.Data.hight)     
    elif name is "stride_x":
        sh.Data.stride_x = val
        print_info(name, sh.Data.stride_x) 
    elif name is "stride_y":
        sh.Data.stride_y = val
        print_info(name, sh.Data.stride_y)   
    elif name is "ct":
        sh.Data.cycle_time = val
        print_info(name, sh.Data.cycle_time) 
    elif name is "amplitude_y":
        sh.Data.amplitude_y = val
        print_info(name, sh.Data.amplitude_y)
    elif name is "amplitude_x":
        sh.Data.amplitude_x = val
        print_info(name, sh.Data.amplitude_x)   
    elif name is "amplitude_balance":
        sh.Data.amplitude_balance = val
        print_info(name, sh.Data.amplitude_balance) 
    elif name is "amplitude_dodge":
        sh.Data.amplitude_dodge = val
        print_info(name, sh.Data.amplitude_dodge)     
    elif name is "dodge_time":
        sh.Data.dodge_time = val
        print_info(name, sh.Data.dodge_time)   
    elif name is "teta":
        sh.Data.teta = val/10.0
        print_info(name, sh.Data.teta)   
    elif name is "delta":
        sh.Data.delta = val/100.0
        print_info(name, sh.Data.delta) 
    elif name is "rho":
        sh.Data.rho = val/10.0
        print_info(name, sh.Data.rho) 
    elif name is "beziere_hight":
        sh.Data.beziere_hight = val
        print_info(name, sh.Data.beziere_hight) 
    elif name is "cc":
        sh.Data.calc_com_active = (val == 1)
        print_info(name, sh.Data.calc_com_active)    
    elif name is "phase":
        if sh.np.array_equal(sh.Data.phase, [0.75, 0.25, 0.25, 0.75]):
            sh.Data.phase = sh.np.array([0.0, 0.75, 0.25, 0.5])
        else:
            sh.Data.phase = sh.np.array([0.75, 0.25, 0.25, 0.75])
        print "toggled phase to ", sh.Data.phase
    else:
        print "[Error]Could not match value: " + str(name)\
            + ": " + str(val) + " in changeValue()"


def control_thread(name):
    '''Starts threads'''
    
    if name is "basic":
        sh.Data.gait_active = False
        print "started!"
        sh.Data.gait_active = True
        try:
            GaitLoop = threading.Thread(target=motion.gait_loop,)
            GaitLoop.start()
        except Exception as exp:
            print "Failed to start gait (" + str(exp) + ")"
    elif name is "demo":
        sh.Data.gait_active = False
        print "started demo!"
        sh.Data.gait_active = True
        DemoLoop = threading.Thread(target=motion.demo,)
        DemoLoop.start()
    elif name is "calibration":
        sh.Data.gait_active = True
        CalibrationLoop = threading.Thread(target=motion.calibrate_com,)
        CalibrationLoop.start()
    elif name is "plot":
        PlotLoop = threading.Thread(target=sh.plot_data,)
        PlotLoop.start()
    elif name is "stop":
        sh.Data.gait_active = False
        print "stopped"
    elif name is "get_up":
        sh.Data.gait_active = False
        motion.move_legs_to()   # Default argument is inital position
    elif name is "get_down":
        sh.Data.gait_active = False
        motion.move_legs_to([(0.0, 0.0, -50.0), (0.0, 0.0, -50),
                             (0.0, 0.0, -50.0), (0.0, 0.0, -50.0)])
    elif name is "zero":
        sh.Data.gait_active = False
        motion.set_zero_pos()
    elif name is "free":
        sh.Data.gait_active = False
        motion.freeMode()
    elif name is "toggle_gait":
        if sh.Data.gait_active :
            control_thread("stop")
        else:
            #gait was started by website, change stride to zero
            sh.Data.stride_x = 0
            control_thread("basic")
    elif name is "shun":
        motion.shun()
    elif name is "server":
        WebThread = threading.Thread(target=server_handler,args=('start',))
        WebThread.start()
    else:
        print "[Error] Could not match " + str(name)+ " in controlThread()"

if __name__ == "__main__":
    
    
                
    def show_stats():
        print "| support:          " + str(sh.Data.support_ratio) +"\n"\
             +"| com_adjust_x:     " + str(sh.Data.com_adjust[0])+"\n"\
             +"| com_adjust_y:     " + str(sh.Data.com_adjust[1])+"\n"\
             +"| hight:            " + str(sh.Data.hight)+"\n"\
             +"| stride_x:         " + str(sh.Data.stride_x)+"\n"\
             +"| stride_y:         " + str(sh.Data.stride_y)+"\n"\
             +"| cycle_time:       " + str(sh.Data.cycle_time)+"\n"\
             +"| A_dodge:          " + str(sh.Data.amplitude_dodge)+"\n"\
             +"| A_balance:        " + str(sh.Data.amplitude_balance)+"\n"\
             +"| dodge_time:       " + str(sh.Data.dodge_time)+"\n"\
             +"| teta:             " + str(sh.Data.teta)+"\n"\
             +"| delta:            " + str(sh.Data.delta)+"\n"\
             +"| rho:              " + str(sh.Data.rho)+"\n"\
             +"| bez_hight         " + str(sh.Data.bez_hight)+"\n"\
             +"| calcCOM:          " + str(sh.Data.calc_com_active)
            
            
    def server_handler(action):
        '''Controls the server-thread'''
        import quaroServer1 as server
        if action is 'start':
            print "Starting server..."
            server.app.run()
        elif action is 'servc':
            print "closing server..."
            try:
                server.quit()
                print "server closed!"
            except:
                print "server already closed!"
         
    alias = {"sf":      "basic",
             "basic":   "basic",
             "start":   "basic",
             "serv":    "server",
             "server":  "server",
             "ser":     "server",
             "servc":   "servc",
             "close":   "servc",
             "d":       "demo",
             "demo":    "demo",
             "c":       "calibration",
             "calibration": "calibration",
             "calib": "calibration",
             "p":       "plot",
             "plot":    "plot",
             "s":       "stop",
             "stop":    "stop",
             "back":    "get_down",
             "getDown": "get_down",
             "down":    "get_down",
             "raise":   "get_up",
             "getup":   "get_up",
             "getUp":   "get_up",
             "shun":    "shun",
             "z":       "zero",
             "zero":    "zero",
             "f":       "free",
             "free":    "free",
             "phase":   "phase",
             "rot":     "rotation",
             "rotation":"rotation",
             "supp":    "supp",
             "support": "supp",
             "comx":    "comx",
             "com_x":   "comx",
             "COMx":    "comx",
             "comy":    "comy",
             "com_y":   "comy",
             "COMy":    "comy",
             "distribution": "distr",
             "distr":   "distr",
             "hight":   "hight",
             "stride":  "stride_x",
             "stridex": "stride_x",
             "stride_x": "stride_x",
             "stridey": "stride_y",
             "stride_y": "stride_y",
             "ct":      "ct",
             "cycletime": "ct",
             "ay":      "amplitude_y",
             "amplitude_y": "amplitude_y",
             "ax":      "amplitude_x",
             "amplitude_x": "amplitude_x",
             "ab":      "amplitude_balance",
             "amplitude_b": "amplitude_balance",
             "ad":      "amplitude_dodge",
             "amplitude_d": "amplitude_dodge",
             "dt":      "dodge_time",
             "dodgetime": "dodge_time",
             "teta":    "teta",
             "delta":   "delta",
             "rho":     "rho",
             "bh":      "beziere_hight",
             "bezierehight": "beziere_hight",
             "cc":      "cc",
             "calcom":   "cc",
             "phase":   "phase"
            }
    
    actions = {"basic":     (control_thread, "start basic gait"),
               "server":    (control_thread, "start server"),
               "servc":     (server_handler, "close server"),
               "demo":      (control_thread, "start demo"),
               "calibration":     (control_thread, "calibrate the COM"),
               "plot":      (control_thread, "plot current data"),
               "stop":      (control_thread, "stop current threads"),
               "get_down":  (control_thread, "move body down"),
               "get_up":    (control_thread, "move body to init position"),
               "shun":      (control_thread, "set all angles to zero"),
               "phase":     (change_value, "toggle phase"),
               "zero":      (control_thread, "menu to set zeropos")
               }
    
    def show_help():
        '''Prints an explanation of every possible shell-command'''
        def search_for_similar(key):
            text_buffer = "[" + str(key) + "]  "
            text_buffer += (12 - len(text_buffer)) * " "
            for k in alias.keys():
                if k is not key and alias[k] is alias[key]:
                    text_buffer += "/" + str(k)
            return text_buffer
    
        print "\nHelp: \n\n"\
             +"[command]   /alternatives:   explanation "\
             + 50 * "-" + "\n"
        already_shown = []
        for key in alias.keys():
            help_line = ""
            if alias[key] not in already_shown:
                already_shown.append(alias[key])
                help_line += search_for_similar(key)
                help_line += (30-len(help_line)) * " "
                if alias[key] in actions:
                    help_line += actions[alias[key]][1]
                else:
                    help_line += "=val"
                print help_line
        print "\n" + 50 * "-" + "\n"\
             +"If explanation is '=val', value is changeable. F.e. 'ab=10'. "\
             +"Otherwise no argument is needed."
    
    print "+-----------------+\n|  QUARO CONTROL  |\n+-----------------+\n"
    print " 0 ---- 1       A\n"\
         +"  |    |       x|                x-y-plain: teta\n"\
         +"  |    |        |                x-z-plain: delta\n"\
         +"  |    |       (*)--->           y-z-plain: rho\n"\
         +" 2 ---- 3      z    y\n\n"\
         +"Enter 'help' for a list of possible commands!\n"

    # Main loop    
    while True:         
        inp = raw_input("[main]-> ")
        if inp in ["exit","e","q","quit"]:
            sh.Data.gait_active = False
            break
        elif inp[:inp.find('=')] in alias or inp in alias:
            if '=' in inp:
                val = inp[inp.find('=')+1:]
                if val is "":
                    print "Missing value!"
                else:
                    arg = alias[inp[:inp.find('=')]]
                    change_value(arg, val)
            else:
                arg = alias[inp]
                if arg in actions:
                    func = actions[arg][0]
                    func(arg)
                else:
                    print "Missing '='!"
        elif inp in ("stats","statistics"):
            show_stats()
        elif inp in ("help",'h'):
            show_help()    
        else:
            print "There is no command: ", inp

    # Close all connections when quitting the script:
    sh.close_connection()
    try:
        server_handler("servc")
    except:
        pass
