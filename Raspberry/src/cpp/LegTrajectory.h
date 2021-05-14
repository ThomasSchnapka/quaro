#ifndef LEGTRAJECTORY_H
#define LEGTRAJECTORY_H

#include <vector>
#include <iostream>
#include "Coordinates.h"
#include "Coordinate.h"
#include "SingleLegTrajectory.h"
#include "BaseFrameTrajectory.h"
#include "State.h"

class LegTrajectory {
	public:
		LegTrajectory(State* pstate, BaseFrameTrajectory* pcomtrajectory);
		~LegTrajectory();
		Coordinates get_leg_position(float t);
	private:
		State* state;
		BaseFrameTrajectory* bftrajectory;
		std::vector<SingleLegTrajectory> leg;
		std::vector<bool> int_to_bool(int i);
};


#endif
