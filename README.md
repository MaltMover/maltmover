# maltmover
A gantry system like the SpiderCam, that can lift stuff around a room using Inverse Kinematics

## Request formats:

### Set new lenght quadratic:
Update over 12 seconds using this quadratic: 3x<sup>2</sup>+4x+1<br>
`{"time": 12.0, "a": 3.0, "b": 4.0, "c": 1.0}`

### Set new lenght in buffer:
Lenght 10, in 12 seconds:<br>
`{"set_length": 10, "time": 12.0, "force": True}`
### Move pulley to buffer lenght:
`{"run": True}`
### Cancel run from pulley:
`{"run": False}`
### Request pulley current lenght:
`{"send_lenght": True}`

### Set new state for grabber:
For open:<br>
`{"set_open": True}`<br>
For close:<br>
`{"set_open": False}`



## Grid layout
Pulley nums:
![image](https://user-images.githubusercontent.com/32793938/209009362-444277ef-e5a5-4a44-9927-2049bb359b5d.png)


## Led Layout
![image](https://user-images.githubusercontent.com/25373105/209230035-8565d58e-e80b-4538-aedb-5c4ecf2fc1ee.png)
