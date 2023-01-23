#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <Servo.h>

#define servoPin 2 //D4

// WiFi credentials
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

// Set static IP
IPAddress subnet(255, 255, 0, 0);
IPAddress gateway(192, 168, 1, 1);
IPAddress local_IP(192, 168, 1, 68);  //Only change this

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
    if (doc["set_open"]) {
      servo.write(180);
      servoIsOpen = true;
      Serial.println("opening");

    } else {
      servo.write(0);
      servoIsOpen = false;
      Serial.println("closing");
    }

    response["success"] = true;
    serializeJson(response, responseOut);

    server.send(200, "application/json", responseOut);
    return;
  } 
  else if (doc.containsKey("get_state")) {
    if(doc["get_state"]) {
      response["isOpen"] = servoIsOpen;
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
