#include <iostream>
#include <unistd.h>				//Needed for I2C port
#include <fcntl.h>				//Needed for I2C port
#include <sys/ioctl.h>			//Needed for I2C port
#include <linux/i2c-dev.h>		//Needed for I2C port
#include "ContactSensor.h"


int file_i2c;
const int length = 1;
unsigned char buffer[length] = {0};

ContactSensor::ContactSensor(){
    // open i2c bus
    char *filename = (char*)"/dev/i2c-1";
    if ((file_i2c = open(filename, O_RDWR)) < 0){
    	std::cout << "Failed to open the i2c bus";	
    }
    	
    const int addr = 0x8;          
    if (ioctl(file_i2c, I2C_SLAVE, addr) < 0){
    	std::cout << "Failed to connect with FootContactSwitch!";
    }
}

ContactSensor::~ContactSensor() {
    close(file_i2c);
}

int ContactSensor::read_contact_sensor(){
    /*
     * Get data from contact sensor encoded in an int. Must be decoded into
     * a bool array.
     *
     * Inconvenient name because read() is already used in i2c-dev.h
     */
    int result = 0;
    if (read(file_i2c, buffer, length) == length){
    	result = int(buffer[0]);
    }else{
    	std::cout << "[ContactSensor.cpp]Failed to read from the i2c bus!" << std::endl;
    }
    return result;
}
