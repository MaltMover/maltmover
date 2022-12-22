#include <ESP8266WiFi.h>
#include <WiFiClient.h>


// WiFi credentials
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;
char c;
String readString = String(100);
WiFiServer wifiServer(80);

bool ledstate = HIGH;
int pin = 5;

void setup() {

  Serial.begin(9600);
  delay(1000);

  WiFi.begin(ssid, password);
  WiFi.mode(WIFI_STA);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting..");
  }

  Serial.print("Connected to WiFi. IP:");
  Serial.println(WiFi.localIP());
  wifiServer.begin();
}


void loop() {
  WiFiClient client = wifiServer.available();
  digitalWrite(pin, HIGH);
  if (client) {
    ledstate = !ledstate;
    //digitalWrite(5, ledstate);
    Serial.println("Client connected");

    while (client.connected()) {

      while (client.available() > 0) {

        char c = client.read();
        if (readString.length() < 100) {
          readString.concat(c);
        }
        Serial.print(c);


        if (c == '\n') {

          delay(50);
          readString = "";
          client.stop();
        }
      }
    }
  }
}
