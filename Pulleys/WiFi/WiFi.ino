#include <ESP8266WiFi.h>

int ledpin = 5;  // D1

// WiFi credentials 
#include "Secret.h"
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

WiFiServer server(80); // Set web server port number to 80
String header; // Variable to store the HTTP request

// Current time
unsigned long currentTime = millis();
// Previous time
unsigned long previousTime = 0;
// Define server timeout time in miliseconds
const long timeoutTime = 2000;


// Initialize WiFi
void initWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("");
}

void setup() {
  Serial.begin(9600);
  pinMode(ledpin, OUTPUT);
  initWiFi();
  server.begin();
}

void handleRequest(WiFiClient client){
  Serial.println("New Client."); // print a message out in the serial port
  String currentLine = "";       // make a String to hold incoming data from the client
  currentTime = millis();
  previousTime = currentTime;
  while (client.connected() && currentTime - previousTime <= timeoutTime)
  { // loop while the client's connected
      currentTime = millis();
      if (client.available())
      {                           // if there's bytes to read from the client,
          char c = client.read(); // read a byte, then
          Serial.write(c);        // print it out the serial monitor
          header += c;
          if (c == '\n')
          { // if the byte is a newline character
              // if the current line is blank, you got two newline characters in a row.
              // that's the end of the client HTTP request, so send a response:
              if (currentLine.length() == 0)
              {
                  // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
                  // and a content-type so the client knows what's coming, then a blank line:
                  client.println("HTTP/1.1 200 OK");
                  client.println("Content-type:application/json");
                  client.println("Connection: close");
                  client.println();

                  // turns the GPIOs on and off
                  if (header.indexOf("GET /on") >= 0)
                  {
                      Serial.println("Activation signal recieved!");
                      digitalWrite(ledpin, HIGH);
                  }
                  else if (header.indexOf("GET /off") >= 0)
                  {
                      Serial.println("Deactivation signal recieved");
                      digitalWrite(ledpin, LOW);
                  }
                  else if (header.indexOf("GET /timer") >= 0)
                  {
                    Serial.println("TIME: "); 
                  }

                  client.println("{'success': true}");

                  // The HTTP response ends with another blank line
                  client.println();
                  // Break out of the while loop
                  break;
              }
              else
              { // if you got a newline, then clear currentLine
                  currentLine = "";
              }
          }
          else if (c != '\r')
          {                     // if you got anything else but a carriage return character,
              currentLine += c; // add it to the end of the currentLine
          }
      }
  }
  // Clear the header variable
  header = "";
  // Close the connection
  client.stop();
  Serial.println("Client disconnected.");
  Serial.println("");
}

void loop()
{
    WiFiClient client = server.available(); // Listen for incoming clients
    if (client)
    {                                  // If a new client connects,
      handleRequest(client);
    }
}
