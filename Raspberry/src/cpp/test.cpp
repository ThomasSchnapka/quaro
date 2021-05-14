#include <iostream>
#include "LegTrajectory.h"
#include "Coordinates.h"
#include "BaseFrameTrajectory.h"
#include "State.h"

 
//using namespace Eigen;
using namespace std;

int main(){
	
	State state;
	BaseFrameTrajectory bftrajectory(&state);
	LegTrajectory ss = LegTrajectory(&state, &bftrajectory);
	
	float t = 0.1;
	for(float t = 0.0; t<1.0; t += 0.1){
		bftrajectory.update(t);
		cout << t << "-----------" << endl;
		cout << ss.get_leg_position(t) << endl;
	}
	cout << "end" << endl;
}
