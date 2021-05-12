#include <iostream>
#include "SwingSpline.h"
#include "Coordinate.h"
#include "State.h"
 
// Default constructor
SwingSpline::SwingSpline(State* pstate) {
	state = pstate;
	}

// Destructor
SwingSpline::~SwingSpline() {}


Coordinate SwingSpline::get_leg_position(float tn) {
	Coordinate m;
	m << -1, -1, -1;
	return m;
}

void SwingSpline::update_spline(Coordinate liftoff_pos){
	int i = 0;
	// pass
}

