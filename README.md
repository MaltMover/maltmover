# maltmover
A gantry system like the SpiderCam, that can lift stuff around a room using Inverse Kinematics

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



## Grid layout
Pulley nums:
![image](https://user-images.githubusercontent.com/32793938/209009362-444277ef-e5a5-4a44-9927-2049bb359b5d.png)


## Led Layout
![image](https://user-images.githubusercontent.com/32793938/221839271-6b0e50c0-ff64-4f22-bd8a-001ffda9d0f7.png)
