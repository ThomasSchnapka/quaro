#ifndef LEGTRAJECTORY_H
#define LEGTRAJECTORY_H

#include <vector>
#include <iostream>
#include "Coordinates.h"
#include "Coordinate.h"
#include "SingleLegTrajectory.h"
#include "COMTrajectory.h"
#include "State.h"

class LegTrajectory {
	public:
		LegTrajectory(State* pstate, COMTrajectory* pcomtrajectory);
		~LegTrajectory();
		Coordinates get_leg_position(float t);
	private:
		State* state;
		COMTrajectory* comtrajectory;
		std::vector<SingleLegTrajectory> leg;
};


#endif
