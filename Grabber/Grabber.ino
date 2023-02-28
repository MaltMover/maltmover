#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <Servo.h>

#define servoPin 13 //D7

// WiFi credentials
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

// Set static IP
IPAddress subnet(255, 255, 0, 0);
IPAddress gateway(192, 168, 1, 1);
IPAddress local_IP(192, 168, 141, 68);  //Only change this

ESP8266WebServer server(80);  // Init server on port 80
Servo servo;

bool grabberIsOpen = false;  // Is grabber currently open?

void setup() {
  servo.attach(servoPin);

  WiFi.config(local_IP, gateway, subnet);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    // Open/Close while connecting
    delay(400);
    servo.write(120);
    delay(400);
    servo.write(90);
  }

  server.on("/", handleBody);  // run handleBody function when receiving request
  server.begin();

  toggleServo(1, false);  // Open servo grabber slowly
}

void loop() {
  server.handleClient();
}

void handleBody() {
  DynamicJsonDocument doc(1024);       // Init json message buffer
  DynamicJsonDocument response(1024);  // Init json response buffer
  String responseOut;

  if (server.hasArg("plain") == false) {
    response["error"] = "Body not received";
    serializeJson(response, responseOut);
    server.send(400, "application/json", responseOut);  // Send error if no body
    return;
  }

  String message;
  message += server.arg("plain");  // Get request body
  message += "\n";

  // Deserialize json
  DeserializationError error = deserializeJson(doc, message);
  if (error) {
    response["error"] = "JSON error";
    serializeJson(response, responseOut);
    server.send(400, "application/json", responseOut); // Send error if wrong json
    return;
  }

  if (doc.containsKey("set_open")) {
    // If set_open is a key, set the grabber state
    response["success"] = true;
    serializeJson(response, responseOut);
    server.send(200, "application/json", responseOut);
    
    grabberIsOpen = doc["set_open"];
    toggleServo(0, doc["set_open"]);
    return;
  } 
  else if (doc.containsKey("get_state") && doc["get_state"]) {
    response["is_open"] = grabberIsOpen;
    serializeJson(response, responseOut);

    server.send(200, "application/json", responseOut);
    return;
  }

  // Send error if there is no known key
  response["error"] = "Unknown Key";
  serializeJson(response, responseOut);
  server.send(400, "application/json", responseOut);
  return;
}

void toggleServo(int delayTime, bool setOpen) {
  if (setOpen) {
    // Use for loop, to choose speed
    for (int pos = 0; pos <= 120; pos += 2){
      servo.write(pos);
      delay(delayTime);
    }
    return;
  } 
  for (int pos = 120; pos >= 0; pos -= 2){
    servo.write(pos);
    delay(delayTime);
  }
}
