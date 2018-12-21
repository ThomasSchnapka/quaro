'''
Module contains all shared data, manages communication with Arduino and
the simulation and stores/plots sensor data.
'''

__version__ = '1'
__author__ = 'Thomas Schnapka'

import time
import numpy as np

cur_time = lambda: int(round(time.time() * 1000))

class Data:
    '''
    Contains all public data.
    '''
    gait_active = False  # used to control the gait threads
    cycle_time = 1500.0  # time for a whole cylce, in ms
    last_cycle_time = 0.0
    #phase = np.array([0.0,0.75,0.25,0.5])  # leg phase between 0 and 1
    #phase = np.array([0.75,0.0,0.5,0.25])
    phase = np.array([0.75, 0.25, 0.25, 0.75])
    stride_x = 60.0  # distance the COM travels during cycle
    stride_y = 0.0
    leglen = 80.0
    hight = 150.0  # operating hight, must be < 2*legelen
    support_ratio = 0.9
    distribution = 0.5  # how stride is spread around the center
    global_x = np.array([0.0, 0.0, 0.0, 10.0])
    global_y = np.array([0.0, 0.0, 0.0, 0.0])
    global_z = np.array([-50.0, -50.0, -50.0, -50.0])
    com = np.array([0.0, 0.0, 0.0])
    com_adjust = np.array([6.0, -6.0, 0.0])
    com_body = np.array([0.0, 0.0, 0.0])
    com_leg = 6.0  # distance from tip, we assume that the COM is right in the legs axis so that there ist no x and y shift
    mass_body = 1.0  # 0.04*10+0.15 #8 Motors, Raspberry, Arduino, Plastic, Cables
    mass_motor = 0.1 
    calc_com_active = True
    #oszillating A
    amplitude_dodge = 10.0 # Amplitude of moving away COM from unloaded legs
    dodge_time = 0.1 #how early/until when dodge moves away (excluding time leg is unloaded)
    #balancing while not in gait
    amplitude_balance = 0.05
    #geometry
    x_pos = (100, 100, -100, -100) # position of every leg (distance from COM)
    y_pos = (-65, 65, -65, 65)
    #teta_0 = [0.7*np.pi, 0.3*np.pi, 1.3*np.pi, -0.3*np.pi] #real leg positions
    teta_0 = [np.arctan2(x_pos[n],y_pos[n]) for n in range(4)]
    #rotation angle factor, will be multiplied with pi
    teta = 0.0
    delta = 0.0
    rho = 0.0
    #relative hight of highest point of beziere-trajecotrys
    bez_hight = 0.3
    data_logging = True
    data_length = 50
    
    data_acc_x = np.array([0 in range(data_length)])
    data_acc_y = np.array([0 in range(data_length)])
    data_acc_z = np.array([0 in range(data_length)])
    data_x = np.array([0.0 in range(data_length)])
    data_y = np.array([0.0 in range(data_length)])
    data_z = np.array([0.0 in range(data_length)])
    data_gsm = np.array([0.0 in range(data_length)])
    last_data_time = cur_time()
    
    

def apply_rec_data(message):
    def gsm():
        '''Returns the gait stability marging. (Distance of COM to nearest 
        boder of support triangle.
        '''
        def distance(n1, n2):
            x1 = Data.global_x[n1] + Data.x_pos[n1]
            y1 = Data.global_y[n1] + Data.y_pos[n1]
            x2 = Data.global_x[n2] + Data.x_pos[n2]
            y2 = Data.global_y[n2] + Data.y_pos[n2]
            try:
                a = np.sqrt((x1-Data.com[0])**2 + (y1-Data.com[1])**2)
                b = np.sqrt((x2-Data.com[0])**2 + (y2-Data.com[1])**2)
                c = np.sqrt((x1-x2)**2 + (y1-y2)**2)
                m = np.sqrt(np.abs(a**2 - (a*(c/(a+b)))**2))
                return m
            except:
                return 0.0
        dist = np.array([0.0, 0.0])
        dist[0] = distance(0, 3)
        dist[1] = distance(1, 2) 
        return round((dist[0] if dist[0] < dist[1] else dist[1]), 2) 
    
    if (cur_time()-Data.last_data_time) > (Data.cycle_time/Data.data_length): #data sample interval
        for i in range(len(message)):
            if message[i] == "<":
                for n in range(i, len(message)):
                    if message[n] == ">":
                        if message[i+1:i+3] == "ax":
                            Data.data_acc_x = np.append(
                                    Data.data_acc_x[-(Data.data_length-1):],
                                    int(message[i+4:n])) #only 100 elements are stored in each array
                        elif message[i+1:i+3] == "ay":
                            Data.data_acc_y = np.append(
                                    Data.data_acc_y[-(Data.data_length-1):],
                                    int(message[i+4:n]))
                        elif message[i+1:i+3] == "az":
                            Data.data_acc_z = np.append(
                                    Data.data_acc_z[-(Data.data_length-1):],
                                    int(message[i+4:n]))
                        break
        Data.data_x = np.append(
                Data.data_x[-(Data.data_length-1):], Data.global_x[0])
        Data.data_y = np.append(
                Data.data_y[-(Data.data_length-1):], Data.global_y[0])
        Data.data_z = np.append(
                Data.data_z[-(Data.data_length-1):], Data.global_z[0])
        Data.data_GSM = np.append(Data.data_gsm[-(Data.data_length-1):], gsm())
        Data.last_data_time = cur_time()
   
    
def plot_data():
    if not Data.simulation_active:
        from matplotlib import use
        use('Agg')
    import matplotlib.pyplot as plt
    #plt.figure(figsize=(7,20))
    plt.subplot(211)
    plt.plot(Data.data_acc_x, label='acc_x')
    plt.plot(Data.data_acc_y, label='acc_y')
    plt.plot(Data.data_acc_z, label='acc_z')
    plt.title("Acceleration")
    plt.ylabel('Bit')
    plt.legend()
    plt.subplot(212)
    #'''
    plt.plot(Data.data_x, label='x')
    plt.plot(Data.data_y, label='y')
    plt.plot(Data.data_z, label='z')
    plt.legend()
    #plt.vlines(x=np.nonzero(data_z))
    #'''
    #plt.plot(data_x,data_z,data_z,data_x)
    #plt.plot(data_GSM, label='GSM')
    plt.savefig("plot.png")
    print "Plot saved!"
    print "Min. GSM:" + str(np.amin(Data.data_gsm))
    plt.show()
    
try: #if script is run on RB, serial will used, otherwise socket
    import serial
    ser = serial.Serial(port='/dev/ttyACM0',  baudrate=115200, timeout=1)
    ser.isOpen()
    Data.simulation_active = False
    
    def send_data(data, datatype=None):
        '''Stores data in a list and sends it via serial
        Args:
            data: Either tuple which contains the value as well as its datatype
                f.e. ('f1',0) or Numpy-Array with plain values, f.e. [0,0,0,0]
            datatype: if data is Numpy-Array, datatype contains the datatype
                for all passed values
        '''
        trans_data = [] #Nested list in which new data will be stored, f.e.[("f1","0")]
        #checks if data is array or scalar
        if isinstance(data, (np.ndarray,list)):
            for i in range(len(data)):
                typename = str(datatype) + str(i) #converts datatype into a nice string
                trans_data.append((typename, data[i]))
        elif isinstance(data, tuple):
            trans_data.append(data)
        else:
            print "send_data(): Wrong data format! " + str(type(data)) + str(data)
            print "Maybe you forgot to put the data into a tuple?"
        #send data
        for i in range(len(trans_data)):
            message = str(trans_data[i][0])
            if trans_data[i][1] != None: 
                message += ":" + str(round(trans_data[i][1], 3))
            ser.write("<" + message + ">")
        #print transData
        del trans_data[:]
        if Data.data_logging:
            ser.write("<end:>") #tell Arduino to send his stuff
            rec_data() #Arduino sends Data after rec some
        
    def rec_data():
        '''Receives data from Arduino and passes it to apply_rec_data()'''
        try:
            rec = ser.readline()
        except:
            print "Failed to rec data"
            Data.gait_active = False
            return None
        if Data.data_logging:
            apply_rec_data(rec)
    
    def close_connection():
        '''Closes connection to serial, otherwise the port stays blocked'''
        ser.close()
        
        
except:
    import socket
    UDP_IP = "127.0.0.1"
    UDP_PORT_send = 6001
    UDP_PORT_receive = 5007
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT_receive))
    sock.settimeout(1) #timeout if nothing is recieved
    Data.simulation_active = True
    
    def send_data(data, datatype=None):
        '''Stores data in a list and sends it via serial
        Args:
            data: Either tuple which contains the value as well as its datatype
                f.e. ('f1',0) or Numpy-Array with plain values, f.e. [0,0,0,0]
            datatype: if data is Numpy-Array, datatype contains the datatype
                for all passed values
        '''
        trans_data = [] #Nested list in which new data will be stored, f.e.("f1","0")
        #checks if data is array or scalar
        if isinstance(data, (np.ndarray, list)):
            for i in range(len(data)):
                typename = str(datatype) + str(i+1) #converts datatype into a nice string
                trans_data.append((typename, data[i]))
        elif isinstance(data, tuple):
            trans_data.append(data)
        else:
            print "send_data(): Wrong data format! " + str(type(data)) + str(data)
            print "Maybe you forgot to put the data into a tuple?"
        ##sends data
        for i in range(len(trans_data)):
            message = str(trans_data[i][0])
            if trans_data[i][1] != None: 
                message += ":"+str(round(trans_data[i][1], 3))
            try:
                sock.sendto("<" + message + ">", (UDP_IP, UDP_PORT_send))
            except:
                #closed main task
                close_connection()
        #print transData
        del trans_data[:]
        if Data.data_logging:
            #ser.write("<end:>") #tell Arduino to send his stuff
            sock.sendto("<end:>", (UDP_IP, UDP_PORT_send))
            rec_data() #Arduino sends Data after rec some 
            
    def rec_data():
        '''Receives data from simulation and passes it to apply_rec_data()'''
        try:
            rec, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        except:
            print "failed to rec data!"
            Data.gait_active = False
            return None
        apply_rec_data(rec)
        
    def close_connection():
        '''Closes connection to socket, otherwise the port stays blocked'''
        sock.close()
