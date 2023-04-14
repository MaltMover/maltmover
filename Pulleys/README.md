# Pulleys
The code found here will run on a single pulley. For of these are needed to run the MaltMover system

## Secret.h
In order to connect to the shared wifi, an SSID and password are needed.
They are stored in the `Secret.h`, which need to to be created upon upload to ESP.

An example can be seen below
```c
const char *SECRET_SSID = "MaltMover";
const char *SECRET_PASS = "maltmover123";
```


## Request formats:

### Set new length in buffer:
Length 10, with 10 dm/s^2 acceleration and 14 dm/s max speed:<br>
`{"length": 10.0, "acceleration": 10.0, "speed": 14.0}`
### Move pulley to buffer length:
`{"run": True}`
### Cancel run from pulley:
`{"run": False}`
### Request pulley current length:
`{"get_length": True}`

### Set new state for grabber:
For open:<br>
`{"set_open": True}`<br>
For close:<br>
`{"set_open": False}`
### Get state of grabber:
`{"get_state": True}`

## Led Layout
![image](https://user-images.githubusercontent.com/32793938/221839271-6b0e50c0-ff64-4f22-bd8a-001ffda9d0f7.png)
