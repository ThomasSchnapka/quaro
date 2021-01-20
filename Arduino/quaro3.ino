#include "Communication.h"
#include "Body.h"
#include "Accelerometer.h"

Body body;
Accelerometer accelerometer;
Communication communication(&body, &accelerometer);


void setup() {
  body.init();
  communication.init();
}

void loop() {
  communication.receive();
}

