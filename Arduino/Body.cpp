/*
 * See Body.h for description
 * Change the bodys geometrical definitions in the section below
 * Thomas Schnapka 2019
 */

/*
  0 ---- 1            A
   |    |             |
   |    |             |
   |    |     <----(y,x)
  2 ---- 3
*/

#include "Arduino.h"
#include "Leg.h"
#include "Body.h"
#include "EEPROM.h"

//pins the servos are attached to, rows ordered by leg number
//collumns are Femur, Tibia and Coxa
const int leg_pin[][3] = {{ 22,  24,  26},
                          { 28,  30,  32},
                          { 34,  36,  38},
                          { 40,  42,  44}};



Body::Body(){
  //make sure all outputs are low to prevent unintended motion
  for(int i=0; i<3; i++){
    for(int n=0; n<3; n++){
      digitalWrite(leg_pin[i][n], LOW);
    }
  }
}

void Body::init(){
  /*
   *init() replaces the constructor due to Arduinos strange compilation behaviour
   *zero positions are read out of EEPROM, values are checked by leg
   */
  for(int i = 0; i<4; i++){
    leg_[i] = new Leg;
    //assure that saved zero positions are feasible
    int alpha = EEPROM.read(10 + i);
    int beta = EEPROM.read(20 + i);
    int gamma = EEPROM.read(30 + i);
    if((abs(alpha) > 30) || (abs(beta) > 30) || (abs(gamma) > 30)){
      alpha = 0;
      beta = 0;
      gamma = 0;
      Serial.println("[Body::init()] Zeropos in EEPROM unfeasible. Please erase");
    }
    int leg_zero_position[] = {alpha, beta, gamma};
    leg_[i]->init(leg_pin[i], leg_zero_position, i);
  }
}


void Body::setLegPos(int l, float alpha, float beta, float gamma){
  leg_[l]->setAngles(alpha, beta, gamma);
}


void Body::shun(){
  for(int i = 0; i<4; i++){
    leg_[i]->shun();
  }
}

void Body::changeZeroPosition(int l, int joint, int amount){
  Serial.println("Changing zeropos of leg " + String(l) + " joint " + String(joint) + " by " + String(amount));
  int pos = leg_[l]->zero_position_[joint];
  leg_[l]->zero_position_[joint] = pos + amount;
  leg_[l]->shun();
}

void Body::saveZeroPositions(){
  /*
   * first number: joint (Femur: 10, Tibia: 20, Coxa: 30)
   * sencond number: leg number
   * saves angle only if it differs from the stored value
  */
  for (int i = 0; i < 4; i++) {
    EEPROM.update(10 + i, leg_[i]->zero_position_[0]);
    EEPROM.update(20 + i, leg_[i]->zero_position_[1]);
    EEPROM.update(30 + i, leg_[i]->zero_position_[2]);
  }
  Serial.println("saved Zeropos to EEPROM!");
  for (int i = 0; i < 4; i++) {
    Serial.println(String(leg_[i]->zero_position_[0]) + " " + String(leg_[i]->zero_position_[1]) + " " + String(leg_[i]->zero_position_[2]));
  }
}

void Body::eraseZeroPositions(){
  /*
   * first number: joint (Femur: 10, Tibia: 20, Coxa: 30)
   * sencond number: leg number
   * sets the current zero-position to zero
  */
  for (int i = 0; i < 4; i++) {
    EEPROM.update(10 + i, 0);
    EEPROM.update(20 + i, 0);
    EEPROM.update(30 + i, 0);
  }
  Serial.println("erased Zeropos in EEPROM!");
}
