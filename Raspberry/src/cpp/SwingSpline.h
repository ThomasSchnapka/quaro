#ifndef SWINGSPLINE_H
#define SWINGSPLINE_H

#include "Coordinates.h"

class SwingSpline {
	public:
		SwingSpline();
		~SwingSpline();
		Coordinates get_leg_position(float t); 
		void change_spline(int to_be_changed, int liftoff_pos, int t);
};


#endif
