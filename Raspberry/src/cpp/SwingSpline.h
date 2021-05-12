#ifndef SWINGSPLINE_H
#define SWINGSPLINE_H

#include <iostream>
#include "Coordinate.h"
#include "State.h"

class SwingSpline {
	public:
		SwingSpline(State* pstate);
		~SwingSpline();
		Coordinate get_leg_position(float tn); 
		void update_spline(Coordinate liftoff_pos);
	private:
	State* state;
};


#endif
