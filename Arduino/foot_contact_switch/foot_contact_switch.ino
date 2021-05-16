/*  Script for foot contact switches for Quaro Quadruped Robot
    Uses force sensitive resistors (RP-S5-ST from Aliexpress)

    More information can be found here:
    https://www.github.com/ThomasSchnapka/quaro
    https://www.thingiverse.com/thing:4821239


    TODO:
    - add I2C support to establish communication with rpi

    How to calculate the force from the measurements:
    1) From the data on Aliexpress we can approximate:
          R(F) = 13000 / (0.6 + 0.003 * F) where F is given in g (Gramm)
    2) The setups uses a voltage divider, thus we have:
          U_in = U_vcc * R(F) / (R + R(F))
    3) Using this knowledge, we can calculate:
          R_f(U_in) = R0 / ((U_0 / U_in) - 1)
          F(R_f) = ((13000/R_f) - 0.6) / 0.003

    Source for characteristic curve:
    https://de.aliexpress.com/item/32955806832.html?spm=a2g0s.12269583.0.0.1865659dQQ1rJ3

*/
#include "PredictiveFilter.h"
#include <Wire.h>
#define I2C_ADDRESS 0x8

// Hardware setup
const int analog_pins[] = {A3, A2, A1, A0};
const int led_pins[] = {5, 6, 7, 8};
const float R0 = 420e3;                     // resistance in series to FSR

// signal processing variables
const int sampling_time = 4;                   // in ms
const int threshold[] = {60, 150, 150, 160};   // threshold for analog value
const int hysteresis[] = {10, 30, 30, 30};     // hysteresis for leg state estimation
PredictiveFilter predictiveFilter[] = {PredictiveFilter(sampling_time, 0.4, 0.7, R0),
                                       PredictiveFilter(sampling_time, 0.4, 0.7, R0),
                                       PredictiveFilter(sampling_time, 0.4, 0.7, R0),
                                       PredictiveFilter(sampling_time, 0.4, 0.7, R0)};

// system variables
long last_time = 0;                             // for sampling
float force[] = {0, 0, 0, 0};                   // measured force in g (Gramm)
bool leg_state[] = {0, 0, 0, 0};                // leg touching ground or not

void setup() {
  Serial.begin(9600);
  // setup pin states
  for (int i; i < 4; i++) {
    pinMode(analog_pins[i], INPUT);
    pinMode(led_pins[i], OUTPUT);
  }
  pinMode(LED_BUILTIN, OUTPUT);
  setup_lights(4);
  Wire.begin(I2C_ADDRESS);
  Wire.onRequest(requestEvent);
  //Wire.onReceive(receiveEvent);
}

void loop() {
  if ((millis() - last_time) > sampling_time) {
    for (int i = 0; i < 4; i++) {
      get_legstate(i);
    }
    //print_status();
    last_time = millis();
    // using internal LED
    digitalWrite(LED_BUILTIN, (leg_state[0] || leg_state[1] || leg_state[2] || leg_state[3]));
  }
}

void get_legstate(int i){
  // state estimation
  force[i] = predictiveFilter[i].updateState(analogRead(analog_pins[i]));
  // thresholding
  if ((leg_state[i] == true) && (force[i] <= (threshold[i] - hysteresis[i]))) {
    leg_state[i] = false;
    digitalWrite(led_pins[i], LOW);
  } else if ((leg_state[i] == false) && (force[i] >= (threshold[i] + hysteresis[i]))){
    leg_state[i] = true;
    digitalWrite(led_pins[i], HIGH);
  }
}



void print_status(){
  /*print filtered values and resulting leg states*/
  
  Serial.println(String(force[0]) + " " + String(force[1]) + " " + String(force[2]) + " " + String(force[3]) + " " + 
                 String(leg_state[0]) + " " + String(leg_state[1]) + " " + String(leg_state[2]) + " " + String(leg_state[3]));
}

void setup_lights(int cycles){
  // nice blinking lights to arouse attention
  int max_duration = 1000;  //in ms
  for(int c = 0; c<cycles; c++){
    for(int i = 0; i<4; i++){
      digitalWrite(led_pins[i], HIGH);
      delay(max_duration*0.25*0.3);
      digitalWrite(led_pins[i], LOW);
      delay(max_duration*0.25*0.7);
    }
  }
}

void requestEvent(){
  // send leg_state via I2C
  // leg_state is converted to byte
  byte msg = leg_state[0] | (leg_state[1] << 1) | (leg_state[2] << 2) | (leg_state[3] << 3);
  Wire.write(msg);
}

// currently unused
//void receiveEvents(int numBytes){  
//  n = Wire.read();
//}

