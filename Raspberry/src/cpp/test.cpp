#include <iostream>
#include "SwingSpline.h"
#include <Eigen/Dense>
 
using Eigen::MatrixXd;

int main(){
	
	quaro::SwingSpline ss = quaro::SwingSpline();
	
	float t = 0.1;
	int s = ss.get_leg_position(t);
	ss.change_spline(0, 0, 0);
	//int s = 0;
	
	std::cout << s <<" ok";
	std::cout << std::endl;
}
