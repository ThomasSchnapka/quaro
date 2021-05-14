#ifndef COMTRAJECTORY_H
#define COMTRAJECTORY_H

#include "Coordinate.h"
#include "State.h"

class BaseFrameTrajectory {
	public:
		BaseFrameTrajectory(State* pstate);
		~BaseFrameTrajectory();
		Coordinate x_bf;
		Coordinate rpy;
		Coordinate predict_x_bf(float dt);
		void update(float t);
	private:
		State* state;
		float t_last;
};


#endif
