#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <Servo.h>

#define servoPin 13 //D7
#ifdef F_CPU
#undef F_CPU
#define F_CPU 80000000UL
#endif

// WiFi credentials
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

// Set static IP
IPAddress subnet(255, 255, 0, 0);
IPAddress gateway(192, 168, 1, 1);
IPAddress local_IP(192, 168, 141, 68);  //Only change this

ESP8266WebServer server(80);
Servo servo;

bool servoIsOpen = false;

void setup() {
  Serial.begin(9600);
  if (WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("Static IP Configured");
  } else {
    Serial.println("Static IP Configuration Failed");
  }

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Waiting to connect...");
    delay(250);
  }

  Serial.print("\nIP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleBody);
  server.begin();

  servo.attach(servoPin);
  servo.write(0);


}

void loop() {
  server.handleClient();
}


void handleBody() {
  DynamicJsonDocument doc(1024);       // Init json message buffer
  DynamicJsonDocument response(1024);  // Init json response buffer
  String responseOut;

  if (server.hasArg("plain") == false) {
    server.send(200, "text/plain", "Body not received");
    return;
  }

  String message;
  message += server.arg("plain");
  message += "\n";

  // Deserialize json and return if error
  DeserializationError error = deserializeJson(doc, message);
  if (error) {
    return;
  }

  if (doc.containsKey("set_open")) {
    /*if (doc["set_open"]) {
      toggleServo(180, true)
      servoIsOpen = true;

    } else {
      toggleServo(180, false)
      servoIsOpen = false;

    }*/
    
    toggleServo(180, doc["set_open"]);
    servoIsOpen = doc["set_open"];
  
    response["success"] = true;
    serializeJson(response, responseOut);

    server.send(200, "application/json", responseOut);
    return;
  } 
  else if (doc.containsKey("get_state")) {
    if(doc["get_state"]) {
      response["is_open"] = servoIsOpen;
      serializeJson(response, responseOut);

      server.send(200, "application/json", responseOut);
      return;
    }
  }

  Serial.println("Error - request does not contain known key \n");

  response["error"] = "Unknown Key";
  serializeJson(response, responseOut);

  server.send(400, "application/json", responseOut);
  return;
}

void toggleServo(int delayTime, bool setOpen) {
  unsigned long calcDelay = delayTime/180;
  if (setOpen) {
    for (int pos = 0; pos <= 180; pos++){
      servo.write(pos);
      delay(calcDelay);
    }
    return;
  } 
  for (int pos = 180; pos >= 0; pos--){
    servo.write(pos);
    delay(calcDelay);
  }
}