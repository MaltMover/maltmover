#include <ESP8266WiFi.h>

const char *ssid = "MaltMover";
const char *password = "maltmover123";

IPAddress local_IP(192, 168, 4, 1);

IPAddress gateway(192, 168, 4, 9);
IPAddress subnet(255, 255, 255, 0);

void setup()
{
  Serial.begin(9600);
  Serial.println();
  Serial.print("Setting soft-AP configuration ... ");
  Serial.println(WiFi.softAPConfig(local_IP, gateway, subnet) ? "Ready" : "Failed!");
  Serial.print("Setting soft-AP ... ");
  Serial.println(WiFi.softAP(ssid, password) ? "Ready" : "Failed!");
  
  Serial.print("Soft-AP IP address = ");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  Serial.print("[Server Connected] ");
  Serial.println(WiFi.softAPIP());
  delay(500);
}
