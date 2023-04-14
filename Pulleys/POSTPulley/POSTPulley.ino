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

  // Print "waiting to connect" and flashing LEDs until wifi is connected
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(WIFILED, HIGH);
    delay(250);
    Serial.println("Waiting to connect...");
    digitalWrite(WIFILED, LOW);
    delay(250);
  }
  digitalWrite(WIFILED, HIGH); // Makes sure the WIFILED is turned on when wifi

  Serial.print("\nIP address: ");
  Serial.println(WiFi.localIP()); // Prints ip

  server.on("/", handleBody); // Configs webserver

  server.begin(); // Starts webserver
  Serial.println("Server listening \n");
}

void loop() {
  server.handleClient();
}

void handleBody() {
  DynamicJsonDocument doc(1024);       // Init json message buffer
  DynamicJsonDocument response(1024);  // Init json response buffer
  String responseOut;                  // Init response-string

  // Returns if no body received
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

  if (doc.containsKey("run")) { // Checks if "run" is an json key
    if (doc["run"]) { // Checks if the key "run" has a true value
      Serial.println("Run pulleys \n");

      response["success"] = true;
      serializeJson(response, responseOut); // Serializes json object as string

      server.send(200, "application/json", responseOut); // Returns a success to the user/program

      digitalWrite(RUNNINGLED, HIGH);
      digitalWrite(CONFIGLED, LOW);

      // Calls run pulley func, that runs pulley to desired point, while still running webserver
      run_pulley();

      // When not running, turns off RUNNINGLED
      digitalWrite(RUNNINGLED, LOW);

      return;
    }

    Serial.println("Reverts config...");
    revert_config(); // If "run" was false, it reverts the config

    // Returns success as JSON response
    response["success"] = true;
    serializeJson(response, responseOut);

    server.send(200, "application/json", responseOut);

    digitalWrite(CONFIGLED, LOW);

    return;
    
  }

  // Checks if received data has all 3 criteria below
  else if (doc.containsKey("length") && doc.containsKey("speed") && doc.containsKey("acceleration")) {
    // Sets config with the received json and with steps_pr_dm
    set_config(doc, steps_pr_dm);

    // Returns success as JSON response
    response["success"] = true;
    serializeJson(response, responseOut);

    server.send(200, "application/json", responseOut);

    digitalWrite(CONFIGLED, HIGH);
    return;
  }

  else if (doc.containsKey("get_length")) {
    if (doc["get_length"]) { // Checks if get_length is present and true
      Serial.println("Send length \n");

      // Returns current length in dm and success as a JSON response
      response["success"] = true;
      response["length"] = stepper.currentPosition() / steps_pr_dm;
      serializeJson(response, responseOut);

      server.send(200, "application/json", responseOut);
      return;
    }
  }

  // Checks if move steps is present
  // Dev feature only and just used for testing/calibrating
  // Moves the stepper without need for confirmation
  else if (doc.containsKey("move_steps")) {
      stepper.move(doc["move_steps"]);

      // Returns success true, as json
      response["success"] = true;
      serializeJson(response, responseOut);
      server.send(200, "application/json", responseOut);

      digitalWrite(RUNNINGLED, HIGH);
      run_pulley(); // Runs pulley to desired point
      digitalWrite(RUNNINGLED, LOW);

      return;
  }

  // Checks if "steps_pr_dm"
  // Feature for setting the steps_pr_dm without need to upload new code
  else if (doc.containsKey("steps_pr_dm")) {
      steps_pr_dm = (double) doc["steps_pr_dm"];
      response["success"] = true;
      serializeJson(response, responseOut);
      server.send(200, "application/json", responseOut);
      return;
  }

  // If received json does not match any if-statements
  Serial.println("Error - request does not contain known key \n");

  // Returns error as JSON with error code 400
  response["error"] = "Unknown Key";
  serializeJson(response, responseOut);

  server.send(400, "application/json", responseOut);
  return;
}
