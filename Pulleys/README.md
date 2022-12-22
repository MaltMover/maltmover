# Secret.h
In order to connect to the shared wifi, an SSID and password are needed.
They are stored in the `Secret.h`, which need to to be created upon upload to ESP.

An example can be seen below
```c
const char *SECRET_SSID = "MaltMover";
const char *SECRET_PASS = "maltmover123";
```