/*
 *  Filter for foot contact switches. 
 *  
 *  Firstly, the analogValue reading is filtered using a discrete LP with
 *  coefficients alpha_u. The voltage reading is converted into a force
 *  asuming a given physical model. Sn extended Kalman Filter is applied 
 *  on this force with filter coefficient alpha_f. The prediction value is
 *  estimated by linear interpolation.
 */


#include "Arduino.h"
#include "PredictiveFilter.h"

PredictiveFilter::PredictiveFilter(float time_step, float alpha_u, float alpha_f, float R0){
  
  _time_step = time_step;
  _alpha_u = alpha_u;
  _alpha_f = alpha_f;
  _R0 = R0;
  _u_last = 0;
  _f_last = 0;
  _f_next = 0;
  _slope  = 0;
}

float PredictiveFilter::updateState(int u_meas){
  // low-pass filter the voltage
  u_meas = _alpha_u*u_meas + (1 - _alpha_u)*_u_last;
  _u_last = u_meas;
  // predictive filtering of force
  _f_last = _f_next;
  float f_pred = _f_last + _slope*_time_step;
  _f_next = _alpha_f*voltage2force(u_meas) + (1-_alpha_f)*f_pred;
  //_f_next = max(0, _f_next);
  calcSlope();
  return _f_next;
}

void PredictiveFilter::calcSlope(){
  // linearized model, calculates slope at current state
  _slope = (_f_next - _f_last)/_time_step;
}

float PredictiveFilter::voltage2force(int u_meas){
  // Physical model, calculates force from measured voltage
  // Equations are derived empirically assuming RP-S5-ST FSRs
  float r = _R0 / ((1024.0 / u_meas) - 1.0);
  float f = 200 + ((13000/r) - 0.6) / 0.003;
  //Serial.println(String(u_meas) + " " + String(r) + " " + String(f));
  return f;
}

