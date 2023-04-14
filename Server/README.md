# Control interface

## Settings
The settings in `config.json` do this:
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

![image](https://user-images.githubusercontent.com/32793938/231967942-2e032700-6813-4f61-8647-9a2259454ffb.png)
