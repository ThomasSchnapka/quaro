/*
 * Body.h - [insert description]
 * handles EEPROM
 * Thomas Schnapka 2019
 * TO-DO:
 */

#ifndef Body_h
#define Body_h

#include "Arduino.h"
#include "Leg.h"
#include "EEPROM.h"

class Body{
  private:
    Leg *leg_[4];
  public:
    Body();
    void init();
    void refresh();
    void shun();
    void setLegPos(int, float, float, float);
    void changeZeroPosition(int, int, int);
    void saveZeroPositions(); //save zeropositions to EEPROM
    void eraseZeroPositions();
};

#endif
