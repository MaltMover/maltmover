<p align="center">
  <img src="https://github.com/MaltMover/maltmover/blob/main/Server/images/crane.png" style="width: 10%" alt="maltmover"/>
</p>

<h1 align="center">MaltMover</h1>
<p align="center"> A gantry system like the SpiderCam, that can reposition objects in a room using Inverse Kinematics</p>

<p align="center">
  <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/MaltMover/maltmover?color=red">
  <a href="https://github.com/MaltMover/maltmover/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/MaltMover/maltmover"></a>
  <img alt="ESP8266" src="https://img.shields.io/badge/MicroController-ESP8266-rgb(255,%20215,%200)">
  <img alt="C++" src="https://img.shields.io/badge/-C%2B%2B-rgb(219,%2055,%20203)">
  <a href="https://python.org"><img alt="Python 3.10" src="https://img.shields.io/badge/python-3.10%20%7C%203.11-blue"></a>
  <a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-black"></a>
</p>

# Installation
Start by uploading the pulley code to all of the pulleys. We have to change the static IP address when uploading, so they don't all get the same address.
To do this navigate to the pulley code:
```bash
cd Pulleys/POSTPulley/
```
and edit the last number on this line:
```c++
IPAddress local_IP(192, 168, 4, 69);  //Only change this
```
As long as a value in the range 0-255 is used, it does not matter, but the correct values should be stored in `Server/config.json`

Now we are ready to install the python dependencies and run the program:
```bash
python -m pip install -r requirements.txt
cd Server/
python main.py
```


# Resources
The MaltMover system consist of multiple parts. All models and diagrams are freely accessible [here](https://drive.google.com/drive/folders/1pCBQdqCMux7k-YYwpfTq4ijKMqQ0Y-yf?usp=share_link). Clicking any of the below pictures will let you download any resources used to create it.

## 3D Models
The MaltMover hardware uses both steel and 3D printed parts. All parts colored blue on this render are 3D printed.


<a href="https://drive.google.com/drive/folders/1qzkBXYEvscYtyos7S_VAo2ytms7zgHjh?usp=share_link"><img alt="MaltMover 3D model" src="https://user-images.githubusercontent.com/32793938/231972383-1a49fd21-c05f-41de-a45c-1aa60a1fcfde.png" style="width: 50%"></a>


## Electrical diagrams
The MaltMover system used four identical PCBs, the diagrams for these can be found below.

<a href="https://drive.google.com/drive/folders/1IsWnVXTo5KvXZRKMOOIyqDj1Af5hVqMQ?usp=sharing"><img alt="MaltMover electrical diagram" src="https://user-images.githubusercontent.com/32793938/231974598-fba7e8d9-b9d5-431d-afff-40060a33ad53.png" style="width: 50%"></a>

A possible PCB with this diagram can be layed out like this:

<a><img alt="MaltMover PCB diagram" src="https://user-images.githubusercontent.com/32793938/231976041-8c771256-e330-4b80-b8c2-fc3bddaa7e5b.png" style="width: 50%"></a>
