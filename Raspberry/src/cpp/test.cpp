#include <iostream>
#include "SwingSpline.h"
#include "Coordinates.h"

 
//using namespace Eigen;
using namespace std;

int main(){
	
	SwingSpline ss = SwingSpline();
	
	float t = 0.1;
	Coordinates s = ss.get_leg_position(t);
	//ss.change_spline(0, 0, 0);
	//int s = 0;
	cout << s << endl;
	cout << s(0, 0) << endl;
	
	//Matrix<float, 3, 4> m;
	//Coordinates m;
	//m << 0, 0, 0, 0,
	//	 0, 0, 0, 0,
	//	 0, 0, 0, 0;
	
	//cout << m << endl;
}
