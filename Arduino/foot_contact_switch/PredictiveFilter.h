#ifndef PredictiveFilter_h
#define PredictiveFilter_h

#include "Arduino.h"

class PredictiveFilter{
  private:
    void calcSlope();
    float voltage2force(int);
    int _u_last;
    float _f_last;
    float _f_next;
    float _slope;
    float _time_step;
    float _alpha_u;
    float _alpha_f;
    float _R0;
    
  public:
    PredictiveFilter(float, float, float, float);
    float updateState(int);
};


#endif
