#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>


// WiFi credentials
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;


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

  if (server.hasArg("plain") == false) {  

    server.send(200, "text/plain", "Body not received");
    return;
  }

  String message = "Body received:\n";
  message += server.arg("plain");
  message += "\n";

  server.send(200, "text/plain", message);
  Serial.println(message);
}

