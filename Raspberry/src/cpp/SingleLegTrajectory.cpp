#include <iostream>
#include <cmath>
#include "SingleLegTrajectory.h"
#include "Coordinate.h"
#include "State.h"
#include "SwingSpline.h"
#include "COMTrajectory.h"
 

SingleLegTrajectory::SingleLegTrajectory(State* pstate,
										 COMTrajectory* pcomtrajectory,
										 int pnum) 
										 : swingspline(pstate)
										 {
	state = pstate;
	comtrajectory = pcomtrajectory;
	num = pnum;
	
	liftoff_pos << 0, 0, 0;
	touchdown_pos << 0, 0, 0;
	current_pos << 0, 0, 0;
	com_at_touchdown << 0, 0, 0;
	fsm = 0;
	
	
	
}

SingleLegTrajectory::~SingleLegTrajectory() {}


Coordinate SingleLegTrajectory::get_leg_position(float t) {
	// normalized time
	float tn = std::fmodf((t+state->phase(num)), 1.0);
	update_fsm(tn);
	
	Coordinate c;
	// retrieve current leg position depending on state
	if(fsm==0){
		c = comtrajectory->x_com;		// subtraction in a single line results in a compilation error
		c -= com_at_touchdown;
	}else{
		c = swingspline.get_leg_position(tn);
	}
	return c;
}

void SingleLegTrajectory::update_fsm(float tn){
	// see doc for finite statemachine
    // 0 = stance
    // 1 = ascending
    // 2 = descending
    
	        if(fsm == 0 & tn >= state->support_ratio){
		fsm = 1;
		swingspline.update_spline(current_pos);
	} else if (fsm == 1 & tn >= state->support_midpoint){
		fsm = 2;
	} else if (fsm == 2 & tn < state->support_ratio){				// CALL CONTACT SENSOR HERE
		fsm = 0;
		update_touchdown_pos();
	}
}

void SingleLegTrajectory::update_touchdown_pos(){
	// save COM position as leg touches ground
	com_at_touchdown = comtrajectory->x_com;
}	
    
