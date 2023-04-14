# maltmover
A gantry system like the SpiderCam, that can lift stuff around a room using Inverse Kinematics

![Lines of code](https://img.shields.io/tokei/lines/github/MaltMover/maltmover?color=red)  ![GitHub](https://img.shields.io/github/license/MaltMover/maltmover) ![ESP](https://img.shields.io/badge/MicroController-ESP8266-rgb(255,%20215,%200)) ![Cpp](https://img.shields.io/badge/-C%2B%2B-rgb(219,%2055,%20203))  ![Version](https://img.shields.io/badge/python-3.10-blue)  ![Style](https://img.shields.io/badge/code%20style-black-black) 

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

## Settings
The settings can be found in `Server/config.json`
| Option                  | Unit       | Function                                                                                                         |
|-------------------------|------------|------------------------------------------------------------------------------------------------------------------|
| edge_limit              | dm         | The closest the object is allowed to get to the edge of the defined area                                         |
| init                    |            |                                                                                                                  |
| - speed                 | dm/s       | Maximum speed during initial extension and final retraction of ropes                                             |
| - acceleration          | dm/s/s     | Acceleration during initial extension and final retraction of ropes                                              |
| max_speed               | dm/s       | Maximum speed reached by a single pulley during normal use of the MaltMover                                      |
| max_acceleration        | dm/s/s     | Acceleration used by all pulleys during normal use of the MaltMover                                              |
| rope_length             | dm         | Length of rope attached to the pulleys, insures no fatal error                                                   |
| three_point_move        | bool       | True if the system should move to three different points, instead of a straight line from a to b                 |
| three_point_delay       | s          | Delay between each of the three moves, if three_point_move is set to true                                        |
| length_offset           | dm         | Difference between actual length of the ropes, and percieved length by the system (size of the carabiner)        |
| size                    | dm\*dm\*dm | Size of the area, the MaltMover works within. (x, y, z)                                                          |
| ips                     | string     | IP addresses of the four pulleys                                                                                 |
| grabber_ip              | string     | IP address if the MaltGrabber                                                                                    |
| grabber_corner_distance | string     | Distance shown on the image below                                                                                |
| steps_pr_dm             | float      | calibrated steps_pr_dm value for each pulley.                                                                    |

#### grabber_corner_distance
![image](https://user-images.githubusercontent.com/32793938/231836288-831a0dc6-23f1-40ea-8c44-8f729cd65514.png)


## Grid layout
Pulley nums:
![image](https://user-images.githubusercontent.com/32793938/209009362-444277ef-e5a5-4a44-9927-2049bb359b5d.png)


## Led Layout
![image](https://user-images.githubusercontent.com/32793938/221839271-6b0e50c0-ff64-4f22-bd8a-001ffda9d0f7.png)
