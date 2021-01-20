#include "Arduino.h"
#include "Accelerometer.h"

#define ACC_PIN_X A0
#define ACC_PIN_Y A1
#define ACC_PIN_Z A2


void Accelerometer::getData(){
  // accleration is returned as array in string, the unit is g-force*10^-3
  int acc[3];
  /*
  for(int p = 0; p<3; p++){
    acc[p] = map(analogRead(pins[p]), 0, 1023, -3000, 3000);
  }
  */
  acc[0] = map(analogRead(ACC_PIN_X), 0, 1023.0*(3.0/5), -3600, 3600);
  acc[1] = map(analogRead(ACC_PIN_Y), 0, 1023.0*(3.0/5), -3600, 3600);
  acc[2] = map(analogRead(ACC_PIN_Z), 0, 1023.0*(3.0/5), -3600, 3600);
}

