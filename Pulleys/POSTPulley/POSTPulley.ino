#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

// Include other files
#include "Helpers.h"
#include "Pulleys.h"
#include "Calibrate.h"
#include "Config.h"

// WiFi credentials
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

// Set static IP
IPAddress subnet(255, 255, 0, 0);
IPAddress gateway(192, 168, 1, 1);
IPAddress local_IP(192, 168, 1, 69);  //Only change this

// Global vars
double currentLength = 0;
double preparedLength = -1;
double preparedTime = -1;
StaticJsonDocument<512> quadConfig;

bool useQuadratic = true;

ESP8266WebServer server(80);

void setup() {

  Serial.begin(9600);
  
  //Setup LED's
  pinMode(WIFILED, OUTPUT);
  pinMode(ALIVELED, OUTPUT);
  pinMode(CONFIGLED, OUTPUT);
  pinMode(RUNNINGLED, OUTPUT);


  digitalWrite(ALIVELED, HIGH);


  calibrate();  // stops execution of code until pulley is calibrated

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
    if (useQuadratic) {

      

      response["success"] = true;
      serializeJson(response, responseOut);

      server.send(200, "application/json", responseOut);

      return;
    } 
    else {
      if (doc["run"]) {
        Serial.println("Run pulleys \n");

        response["success"] = true;
        serializeJson(response, responseOut);

        server.send(200, "application/json", responseOut);

        digitalWrite(RUNNINGLED, HIGH);
        digitalWrite(CONFIGLED, LOW);
        
        runPulleys(preparedLength, preparedTime, &currentLength); // Is run later than success, since it holds up the execution of code

        digitalWrite(RUNNINGLED, LOW);
        
        useQuadratic = true;

        return;
      }

      Serial.println("Reverts config...");
      revertConfig(currentLength, &preparedLength, &preparedTime);

      response["success"] = true;
      serializeJson(response, responseOut);

      server.send(200, "application/json", responseOut);

      digitalWrite(CONFIGLED, LOW);

      useQuadratic = true;

      return;
    }
  }

  else if (doc.containsKey("length") && doc.containsKey("time") && doc.containsKey("force")) {
    double length = doc["length"];
    double time = doc["time"];
    bool force = doc["force"];

    if (force) {
      setConfig(length, time, &preparedLength, &preparedTime);

      response["success"] = true;
      serializeJson(response, responseOut);

      server.send(200, "application/json", responseOut);

      digitalWrite(CONFIGLED, HIGH);

      useQuadratic = false;
    }

    response["success"] = false;
    response["error"] = "Force must be true, otherwise deprecated.";
    serializeJson(response, responseOut);
    server.send(200, "application/json", responseOut);
    return;
  }

  else if (doc.containsKey("time") && doc["a"] && doc["b"] && doc["c"]) {
    quadConfig = setQuadraticConfig(doc);
    useQuadratic = true;

    response["success"] = true;
    serializeJson(response, responseOut);
    server.send(200, "application/json", responseOut);
    return;
  }

  else if (doc.containsKey("send_length")) {
    if (doc["send_length"]) {
      Serial.println("Send length \n");

      response["success"] = true;
      response["length"] = currentLength;
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
