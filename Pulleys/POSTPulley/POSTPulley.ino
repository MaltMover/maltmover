#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

// WiFi credentials
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;


IPAddress subnet(255, 255, 0, 0);			            
IPAddress gateway(192, 168, 1, 1);			            
IPAddress local_IP(192, 168, 1, 69);	


double currentLength = 0;
double preparedLength = -1;
double preparedTime = -1;

ESP8266WebServer server(80);

void setup() {

  Serial.begin(9600);

  calibrate(); // stops execution of code until pulley is calibrated

  if (WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("Static IP Configured");
  }
  else {
    Serial.println("Static IP Configuration Failed");
  }

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.println("Waiting to connect...");
  }

  Serial.print("\nIP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleBody);

  server.begin();
  Serial.println("Server listening \n");
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

  // Deserialize json and return if error
  DeserializationError error = deserializeJson(doc, message);
  if (error)
    return;
  if (doc.containsKey("run")) {
    if (doc["run"]) {
      Serial.println("Run pulleys \n");

      runPulleys();
      server.send(200, "application/json", "{\"success\": true}");
      return;
    }

    Serial.println("Reverts config...");
    revertConfig();
    server.send(200, "application/json", "{\"success\": true}");
    return;
  }
  else if (doc.containsKey("length") && doc.containsKey("time")) {
    double length = doc["length"];
    double time = doc["time"];
    server.send(200, "application/json", "{\"success\": true}");
    setConfig(length, time);
    return;
  }
  else if (doc.containsKey("send_length")) {
    if (doc["send_length"]) {
      Serial.println("Send length \n");
      server.send(200, "application/json", "{\"success\": true, \"length\": 69.4}");
      return;
    }
  }
  Serial.println("Error - request does not contain known key \n");
  server.send(400, "application/json", "{\"error\": \"Unknown key\"}");
  return;
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

  Serial.println("Reverted config to original state \n");
  return;
}

void runPulleys() {
  // add code to run pulleys
  return;
}


void calibrate() {
  // add code to calibrate length of wire
  //delay(5000);
  return;
}
