#include <iostream>
#include <cmath>
#include "SingleLegTrajectory.h"
#include "Coordinate.h"
#include "State.h"
#include "SwingSpline.h"
#include "BaseFrameTrajectory.h"
 

SingleLegTrajectory::SingleLegTrajectory(State* pstate,
										 BaseFrameTrajectory* pcomtrajectory,
										 int pnum) 
										 : swingspline(pstate, pcomtrajectory)
										 {
	state = pstate;
	bftrajectory = pcomtrajectory;
	num = pnum;
	
	liftoff_pos << 0, 0, 0;
	current_pos << 0, 0, 0;
	leg_at_touchdown << 0, 0, 0;
	com_at_touchdown << 0, 0, 0;
	fsm = 0;
	
	
	
}

SingleLegTrajectory::~SingleLegTrajectory() {}


Coordinate SingleLegTrajectory::get_leg_position(float t) {
	// normalized time
	float tn = std::fmodf((t+state->phase(num)), 1.0);
	update_fsm(tn);
	
	
	// retrieve current leg position depending on state
	Coordinate c;
	if(fsm==0){
		c = get_position_stance();
	}else{
		c = swingspline.get_leg_position(tn);
	}
	current_pos = c;
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
	leg_at_touchdown = current_pos;
	com_at_touchdown = bftrajectory->x_com;
}	

Coordinate SingleLegTrajectory::get_position_stance(){
	// pos = leg_at_touchdown - (bftrajectory->x_com - com_at_touchdown)
	// subtraction in a single line results in compilation error,
	// that it is done in seperate lines
	Coordinate c = leg_at_touchdown;
	c -= bftrajectory->x_com;
	c += com_at_touchdown;
	return c;
}
    
