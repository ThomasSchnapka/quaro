#ifndef Communication_h
#define Communication_h

#include "Arduino.h"
#include "Body.h"
#include "Accelerometer.h"


class Communication{
  private:
    void sendData();
    void applyNewData(char[], int);
    char receivedChars[32]; //message may contain up to 32 characters
    Body* body_;
    Accelerometer* accelerometer_;
  public:
    void receive();
    Communication(Body*, Accelerometer*);
    void init(); //replacement for constructor
};

#endif
