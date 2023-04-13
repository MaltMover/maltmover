#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <AccelStepper.h>

// Include other files
#include "Helpers.h"
#include "Pulleys.h"
#include "Calibrate.h"
#include "Config.h"
#include "Globals.h"

// WiFi credentials
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

// Set static IP

IPAddress gateway(192, 168, 4, 1);
IPAddress local_IP(192, 168, 4, 71);  //Only change this
IPAddress subnet(255, 255, 0, 0);

AccelStepper stepper(AccelStepper::FULL4WIRE, IN1, IN2, IN3, IN4);
ESP8266WebServer server(80);

double steps_pr_dm = 130;  // Default value for steps_pr_dm, changed with POST requests

void setup() {
  Serial.begin(9600);

  //Setup LED's
  pinMode(WIFILED, OUTPUT);
  pinMode(CONFIGLED, OUTPUT);
  pinMode(RUNNINGLED, OUTPUT);

  revert_config();  // Set default config, with low speed and accel

  calibratePulley();  // stops execution of code until pulley is calibrated
  
  if (WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("Static IP Configured");
  } else {
    Serial.println("Static IP Configuration Failed");
  }
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(WIFILED, HIGH);
    delay(250);
    Serial.println("Waiting to connect...");
    digitalWrite(WIFILED, LOW);
    delay(250);
  }
  digitalWrite(WIFILED, HIGH);

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

  if (doc.containsKey("run")) {
    if (doc["run"]) {
      Serial.println("Run pulleys \n");

      response["success"] = true;
      serializeJson(response, responseOut);

      server.send(200, "application/json", responseOut);

      digitalWrite(RUNNINGLED, HIGH);
      digitalWrite(CONFIGLED, LOW);
      
      run_pulley();

      digitalWrite(RUNNINGLED, LOW);

      return;
    }

    Serial.println("Reverts config...");
    revert_config();

    response["success"] = true;
    serializeJson(response, responseOut);

    server.send(200, "application/json", responseOut);

    digitalWrite(CONFIGLED, LOW);

    return;
    
  }

  else if (doc.containsKey("length") && doc.containsKey("speed") && doc.containsKey("acceleration")) {
    set_config(doc, steps_pr_dm);

    response["success"] = true;
    serializeJson(response, responseOut);

    server.send(200, "application/json", responseOut);

    digitalWrite(CONFIGLED, HIGH);
    return;
  }

  else if (doc.containsKey("get_length")) {
    if (doc["get_length"]) {
      Serial.println("Send length \n");

      response["success"] = true;
      response["length"] = stepper.currentPosition() / steps_pr_dm;
      serializeJson(response, responseOut);

      server.send(200, "application/json", responseOut);
      return;
    }
  }

  else if (doc.containsKey("move_steps")) {
      stepper.move(doc["move_steps"]);

      response["success"] = true;
      serializeJson(response, responseOut);
      server.send(200, "application/json", responseOut);

      digitalWrite(RUNNINGLED, HIGH);
      run_pulley();
      digitalWrite(RUNNINGLED, LOW);

      return;
  }

  else if (doc.containsKey("steps_pr_dm")) {
      steps_pr_dm = (double) doc["steps_pr_dm"];
      response["success"] = true;
      serializeJson(response, responseOut);
      server.send(200, "application/json", responseOut);
      return;
  }

  Serial.println("Error - request does not contain known key \n");

  response["error"] = "Unknown Key";
  serializeJson(response, responseOut);

  server.send(400, "application/json", responseOut);
  return;
}
