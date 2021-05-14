#ifndef SINGLELEGTRAJECTORY_H
#define SINGLELEGTRAJECTORY_H

#include <iostream>
#include "Coordinate.h"
#include "State.h"
#include "SwingSpline.h"
#include "BaseFrameTrajectory.h"

class SingleLegTrajectory {
	public:
		SingleLegTrajectory(State* pstate, BaseFrameTrajectory* pcomtrajectory, int pnum);
		~SingleLegTrajectory();
		Coordinate get_leg_position(float t);
		
		Coordinate liftoff_pos;
		Coordinate current_pos;
		Coordinate leg_at_touchdown;
		Coordinate com_at_touchdown;
		
		//SwingSpline(State* pstate) : swingspline(pstate) {}
		SwingSpline swingspline;
		
	private:
		State* state;
		BaseFrameTrajectory* bftrajectory;
		int num; 		// leg number
		int fsm;
		
		void update_fsm(float tn);
		void update_touchdown_pos();
		Coordinate get_position_stance();
		
	
		
};


#endif
