/*  Script for foot contact switches for Spotmicro Quadruped Robot
    Uses force sensitive resistors

    More information can be found here:
    https://www.github.com/ThomasSchnapka/quaro
    https://www.thingiverse.com/thing:4821239

    AS I HAVE TO WAIT FOR THE REMAINING SENSORS TO BE DELIVERED,
    THIS SCRIPT IS NOT TESTED WITH THE WHOLE SETUP!
    However the function of the setup can be verified using the
    serial plot function of Arduino IDE

    TODO:
    - add I2C support to establish communication with rpi
    - test script with whole setup

*/

// Hardware setup
const int analog_pins[] = {A0, A1, A2, A3};
const int led_pins[] = {0, 1, 2, 3};

// signal processing settings
const int sampling_rate = 10;                   // in ms
const float alpha = 0.5;                        // filter coefficient
const int threshold[] = {500, 500, 500, 500};   // threshold for analog value

// system variables
long last_time = 0;                             // for sampling
int last_val[] = {0, 0, 0, 0};                  // used for filter
bool leg_state[] = {0, 0, 0, 0};                // leg touching ground or not

void setup() {
  Serial.begin(9600);
  // setup pin states
  for (int i; i < 4; i++) {
    pinMode(analog_pins[i], INPUT);
    pinMode(led_pins[i], OUTPUT);
  }
}

void loop() {
  if ((millis() - last_time) > sampling_rate) {
    for (int i; i < 4; i++) {
      get_legstate(i);
    }
    print_status();
    last_time = millis();
  }
}

void get_legstate(int i){
  /*get analog value, filter and threshold it*/
  int val = analogRead(analog_pins[i]);
  // simple LP filtering
  val = alpha * val + (1 - alpha) * last_val[i];
  last_val[i] = val;
  
  // thresholding
  if (val > threshold[i]) {
    leg_state[i] = false;
    digitalWrite(led_pins[i], LOW);
  } else {
    leg_state[i] = true;
    digitalWrite(led_pins[i], HIGH);
  }
}

void print_status(){
  /*print filtered values and resulting leg states*/
  Serial.println(String(last_val[0])  + " " + String(last_val[1])  + " " + String(last_val[2])  + " " + String(last_val[3]) + " " +
                 String(leg_state[0]) + " " + String(leg_state[1]) + " " + String(leg_state[2]) + " " + String(leg_state[3])   );
}

