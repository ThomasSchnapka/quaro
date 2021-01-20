/*
   See Leg.h for description
   Change the legs geometrical definitions in the section below
   Thomas Schnapka 2019
*/

//geometrical definitions
#define MAX_FEMUR 45
#define MIN_FEMUR -45
#define MAX_TIBIA 90
#define MIN_TIBIA -90
#define MAX_COXA 30
#define MIN_COXA -30

//change the following parameters based on the results of servocalibration
#define PULSEWIDTH_MIN 960.0 //at -45 DEG
#define PULSEWIDTH_MAX 2020.0 //at 45 DEG


#include "Arduino.h"
#include "Servo.h"
#include "Leg.h"

//calculation of linear equation using the values above
const float SLOPE_PULSEWIDTH = ((PULSEWIDTH_MAX - PULSEWIDTH_MIN) / (45 - (-45)));
const float STARTPOINT_PULSEWIDTH = (PULSEWIDTH_MAX - 45 * SLOPE_PULSEWIDTH);

//conversion factor to convert from RAD to DEG
const float CONV = 360.0 / (2.0 * PI);

void Leg::init(int pin[3], int zero_position[3], int number) {
  //the following initialisation cannot be done in Leg constructor due to C++ complilation behavoir
  Femur.attach(pin[0]);
  Tibia.attach(pin[1]);
  Coxa.attach(pin[2]);
  number_ = number;
  for (int i = 0; i < 3; i++) {
    zero_position_[i] = zero_position[i];
  }
}

void Leg::setAngles(float alpha, float beta, float gamma) {

  //check if angles are approachable, currently checked with constant values, may be changed to dynamic verification (as angles depend on each other)
  if (alpha <= MIN_FEMUR) {
    alpha = MIN_FEMUR;
  } else if (alpha >= MAX_FEMUR) {
    alpha = MAX_FEMUR;
  }
  if (beta <= MIN_TIBIA) {
    beta = MIN_TIBIA;
  } else if (beta >= MAX_TIBIA) {
    beta = MAX_TIBIA;
  }
  if (gamma <= MIN_COXA) {
    gamma = MIN_COXA;
  } else if (gamma >= MAX_COXA) {
    gamma = MAX_COXA;
  }
  
  //inverting certain angles because servos are rotated by 180 deg
  if(number_ == 0 || number_ == 2){
    alpha *= -1;
    beta *= -1;
  }
  if(number_ == 2 || number_ == 3){
    gamma *= -1;
  }
  
  write_angle(&Femur, zero_position_[0] + alpha);
  write_angle(&Tibia, zero_position_[1] + beta);
  write_angle(&Coxa, zero_position_[2] + gamma);
}

void Leg::shun(){
  write_angle(&Femur, zero_position_[0]);
  write_angle(&Tibia, zero_position_[1]);
  write_angle(&Coxa, zero_position_[2]);
}

void Leg::write_angle(Servo *servo, float angle) {
  //Serial.println(String(angle));
  if ((isnan(angle) != 1) && (isinf(angle) != 1)) { //check if angle is a real value
    servo->writeMicroseconds(int(STARTPOINT_PULSEWIDTH + SLOPE_PULSEWIDTH * angle));
    //Serial.println(int(STARTPOINT_PULSEWIDTH + SLOPE_PULSEWIDTH*angle));
  } else {
    Serial.println("[Leg::write_angle] Bad value on leg " + String(number_) + ": " + String(angle));
  }
}

