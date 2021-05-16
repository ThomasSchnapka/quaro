#include <iostream>
#include "GaitController.h"
#include "Coordinates.h"
#include "State.h"

 
//using namespace Eigen;
using namespace std;

int main(){
	
	GaitController gc = GaitController();
	
	float t = 0.1;
	for(float t = 0.0; t<1.0; t += 0.1){
		cout << t << "-----------" << endl;
		cout << gc.get_leg_position(t) << endl;
	}
	cout << "end" << endl;
}
