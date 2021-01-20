import time
import numpy as np

class HardwareInterface:
    
    # inner class to fake serial connection and send data to simulation
    class SerialDummy:
        def __init__(self):
            import socket
            self.UDP_IP = "127.0.0.1"
            self.UDP_PORT_send = 6000
            self.UDP_PORT_receive = 5006
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            self.sock.bind((self.UDP_IP, self.UDP_PORT_receive))
            self.sock.settimeout(1) #timeout if nothing is recieved
            
            
        def write(self, text):
            # print(text)
            self.sock.sendto(text , (self.UDP_IP, self.UDP_PORT_send))
            
        def close(self):
            self.sock.close()
            print "[serial] closed"
            
        def readline(self):
            return "<noDataAvailable>"
        
        
    def __init__(self, hardware_config, state):
        self.config = hardware_config
        self.ser = self.open_serial_connection()
        self.angle_cache = np.zeros((3,4))
        self.state = state
        
    def open_serial_connection(self):
        '''
        Try to open serial connection with Arduino
        If not possible, establish connection with serial dummy for testing
        returns serial handle
        '''
        ser = None
        possible_ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2",
                          "/dev/ttyUSB3", "/dev/tty.wchusbserialfd120",
                          "/dev/tty.wchusbserialfa130",
                          "/dev/tty.usbmodemFD121", "/dev/tty.usbmodemFA131"]
        for possible_port in possible_ports:
            try:
                import serial
                ser = serial.Serial(port=(str(possible_port)),
                                    baudrate =int(self.config.serial_baudrate),
                                    timeout = self.config.serial_timeout) 
                print "[serial] opened at " + ser.port
                time.sleep(1) # Arduino needs some time to establish connection
                break
            except:
                pass
        if ser is None:
            # serial connection could not be opened
            print ("[serial] could not open serial! " 
                   "Check ports with 'ls -l /dev/tty*'")
            ser = self.SerialDummy()
            print "[serial] established connection with serial dummy"
            
        return ser
    
        
    def send(self, data):
        self.ser.write("<" + data + ">")
        if self.state.debug_communication:
            print "[serial] sending: <" + data + ">"
        

    def receive(self):
        self.send('s') # request to Arduino to send own data
        rec = self.ser.readline()
        while("<noDataAvailable>" not in rec):
            print "[serial] receiving: " + rec
            rec = self.ser.readline()  
            
        
    def send_angle(self, angle):
        '''
        Input: angles in 3x4 np.array
        Angles get rounded to 2 decimals and send via quaro protocoll
        To reduce the amount of data in serial communication, angles are saved
        and not resendet if they do not change (angle_cache)
        '''
        angle = np.around(angle, 2)
        
        for leg, a in enumerate(angle.T):
            if not np.array_equal(self.angle_cache[:,leg],a):
                self.send(str(leg)+ ':a' + str(a[0])
                                  +  'b' + str(a[1])
                                  +  'g' + str(a[2]))
                self.angle_cache[:,leg] = a
        #tell Arduino to send own data
        self.receive()
        
        
    def send_command(self, cmd):
        self.send(str(cmd))
        
    
    def shutdown(self):
        #Closes connection to serial, otherwise the port stays blocked
        self.ser.close()
        
    #def plot(self):
    #    import matplotlib.pyplot as plt
    #    plt.plot(self.vals)