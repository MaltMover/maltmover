#include <ESP8266WiFi.h>

extern "C" {
  #include<user_interface.h>
}

const char *ssid = "MaltMover";
const char *password = "maltmover123";

IPAddress gateway(192, 168, 4, 0);
IPAddress local_IP(192, 168, 4, 1);
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
  client_status();
  delay(5000);
}

void client_status() {
  unsigned char number_client;
  struct station_info *stat_info;
  
  struct ip4_addr *IPaddress;
  IPAddress address;
  int i=1;
  
  number_client= wifi_softap_get_station_num();
  stat_info = wifi_softap_get_station_info();
  
  Serial.print(" Total Connected Clients are = ");
  Serial.println(number_client);
  
  while (stat_info != NULL) {
  
    IPaddress = &stat_info->ip;
    address = IPaddress->addr;
    
    Serial.print("client= ");
    Serial.print(i);

    Serial.print(" IP adress is = ");
    Serial.print((address));
    
    stat_info = STAILQ_NEXT(stat_info, next);
    i++;
    Serial.println();
  }
  delay(500);
}
