#include <EEPROM.h>
#include "Communication.h"
#include "Arduino.h"
#include "Body.h"

Communication::Communication(Body* body, Accelerometer* accelerometer) {
  body_ = body;
  accelerometer_ = accelerometer;
}

void Communication::init() {
  Serial.begin(115200);
}

void Communication::sendData() {
  //send sensor data if requested by Raspberry
  Serial.println("<noDataAvailable>");
}

void Communication::receive() {
  /*
   * recieves messages from the Raspberry
   * messages are wrapped in <> and may contain a colon : to seperate the value from its name
   * after the message is terminated, applyNewData() gets called
   * messages may contain up to 16 characters
   */
  
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char message;

  while (Serial.available() > 0) { //As long as serial buffer is not empty and there is no new Data to display
    message = Serial.read();
    if (recvInProgress == true) {
      if (message != '>') {
        receivedChars[ndx] = message;
        ndx++;
      } else {
        receivedChars[ndx] = '\0'; //terminate string
        recvInProgress = false;
        applyNewData(receivedChars, ndx);
        ndx = 0;
      }
    }
    else if (message == '<') {
      recvInProgress = true;
    }
  }
}

void Communication::applyNewData(char chars[], int len) {
  //apply received data
  //if message has more than 2 chars, it contains values
  if (len > 2) {
    String message = String(chars);
    int colon = message.indexOf(':');
    String type = message.substring(0, colon);
    String value = message.substring(colon + 1, len);
    if(type == "0" || type == "1" || type == "2" || type == "3"){
      //Coordinates have leg number as type
      //f.e. <3:a-10b0g10.0> sets angles of leg 3 to (-10|0|10)
      int leg = type.toInt();
      float alpha = (value.substring(value.indexOf('a')+1, value.indexOf('b'))).toFloat();
      float beta = (value.substring(value.indexOf('b')+1, value.indexOf('g'))).toFloat();
      float gamma = (value.substring(value.indexOf('g')+1, len)).toFloat();
      body_->setLegPos(leg, alpha, beta, gamma);
    }else if(type == "z"){
      //change zero position
      //f.e. <z:l0j1a-4> decreases zeropos of leg 0 joint 1 by 4
      int leg = (value.substring(value.indexOf('l')+1, value.indexOf('a'))).toInt();
      int joint = (value.substring(value.indexOf('j')+1, value.indexOf('a'))).toInt();
      int amount = (value.substring(value.indexOf('a')+1, len)).toInt();
      body_->changeZeroPosition(leg, joint, amount);
    } else {
      Serial.println("Communication::applyNewData(..) could not resolve " + String(chars) + " with type " + String(type));
    }
  //if message contains up to 2 chars, it is a command without values
  } else {
    if (chars[0] == 's') {
      //request to send sensor data
      sendData();
    } else if (chars[0] == 'b') {
      //check number of chars in buffer
      Serial.println("<b:" + String(Serial.available()) + ">");
    }  else if (chars[0] == 'd') {
      //shun
      body_->shun();
    }  else if (chars[0] == 'q') {
      //save zero positions to EEPROM
      body_->saveZeroPositions();
    }  else if (chars[0] == 'e') {
      //erase positions to EEPROM
      body_->eraseZeroPositions();
    } else {
      Serial.println("Could not resolve [2]" + String(chars));
    }
  }
}



