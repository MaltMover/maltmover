#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

int ledpin = 5;  // D1

// WiFi credentials 
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

// Variable to save current epoch time
unsigned long epochTime; 

// Function that gets current epoch time
unsigned long getTime() {
  timeClient.update();
  unsigned long now = timeClient.getEpochTime();
  return now;
}

void setup() {
  Serial.begin(9600);
  pinMode(ledpin, OUTPUT);
  timeClient.begin();
  server.begin();
}

void loop()
{
    epochTime = getTime();
    Serial.print("Epoch Time: ");
    Serial.println(epochTime);
    if (epochTime % 2 == 0){
      digitalWrite(ledpin, HIGH);
    }
    else{
      digitalWrite(ledpin, LOW);
    }
}
