#include <iostream>
#include "SwingSpline.h"
#include "Coordinates.h"
 
// Default constructor
SwingSpline::SwingSpline() {}

// Destructor
SwingSpline::~SwingSpline() {}

// Return the area of the rectangle
Coordinates SwingSpline::get_leg_position(float t) {
	Coordinates m;
	m << 0, 0, 0, 0,
		 0, 0, 0, 3.1,
		 0, 0, 0, 0;
	return m;
}

void SwingSpline::change_spline(int to_be_changed, int liftoff_pos, int t){
	to_be_changed = liftoff_pos;
}

