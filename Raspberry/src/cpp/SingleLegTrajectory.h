#ifndef SINGLELEGTRAJECTORY_H
#define SINGLELEGTRAJECTORY_H

#include <iostream>
#include "Coordinate.h"
#include "State.h"
#include "SwingSpline.h"
#include "COMTrajectory.h"

class SingleLegTrajectory {
	public:
		SingleLegTrajectory(State* pstate, COMTrajectory* pcomtrajectory, int pnum);
		~SingleLegTrajectory();
		Coordinate get_leg_position(float t);
		
		Coordinate liftoff_pos;
		Coordinate current_pos;
		Coordinate com_at_touchdown;
		
		//SwingSpline(State* pstate) : swingspline(pstate) {}
		SwingSpline swingspline;
		
	private:
		State* state;
		COMTrajectory* comtrajectory;
		int num; 		// leg number
		int fsm;
		
		void update_fsm(float tn);
		void update_touchdown_pos();
		
	
		
};


#endif
