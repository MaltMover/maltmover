#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

// WiFi credentials
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

double currentLength = 0;
double preparedLength = -1;
double preparedTime = -1;

ESP8266WebServer server(80);

void setup() {

  Serial.begin(9600);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.println("Waiting to connect...");
  }

  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleBody);

  server.begin();
  Serial.println("Server listening");
}

void loop() {

  server.handleClient();
}

void handleBody() {
  DynamicJsonDocument doc(1024); // Init json buffer

  if (server.hasArg("plain") == false) {

    server.send(200, "text/plain", "Body not received");
    return;
  }

  String message;
  message += server.arg("plain");
  message += "\n";

  server.send(200, "text/plain", message);
  //Serial.println(message);

  // Deserialize json and return if error
  DeserializationError error = deserializeJson(doc, message);
  if (error)
    return;
  if (doc.containsKey("run")) {
    if (doc["run"]) {
      Serial.println("Run pulleys");

      runPulleys();

      return;
    }

    Serial.println("Reverts config...");
    revertConfig();
  }
  else if (doc.containsKey("length") && doc.containsKey("time")) {
    double length = doc["length"];
    double time = doc["time"];

    setConfig(length, time);
    return;
  }
  
  Serial.println("Error - request does not contain known key");

}

void setConfig(double length, double time){

  preparedLength = length;
  preparedTime = time;

  Serial.print("Prepared length: ");
  Serial.println(preparedLength);
  Serial.print("Prepared time: ");
  Serial.println(preparedTime);
  Serial.println();

  return;

}

void revertConfig() {
  // Runs if recieves "run": false. 
  preparedLength = currentLength;
  preparedTime = -1;

  Serial.println("Reverted config to original state");
}

void runPulleys() {
  // add code to run pulleys
  return;
}

