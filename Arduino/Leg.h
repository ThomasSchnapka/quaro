/*
 * Leg.h - [insert description]
 * Thomas Schnapka 2019
 * TO-DO:
 * zero-position menu (maybe use the code from Quaro7.ino)
 * feedback loop
 * dynamic boundary anngles
 */

#ifndef Leg_h
#define Leg_h

#include "Arduino.h"
#include "Servo.h"

class Leg{
  private:
    friend class Body;
    Servo Femur, Tibia, Coxa;
    void write_angle(Servo*, float);
    void setAngles(float, float, float);
    //feedback_loop();
    int number_;
    int zero_position_[3];
  public:
    void shun();
    void init(int[3], int[3], int); //initialize leg
};

#endif
