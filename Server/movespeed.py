import pandas as pd
import matplotlib.pyplot as plt

from space import Space
from point import Point
from pulley import Pulley

max_length = 1000
max_speed = 1000

size = 100, 100, 100
pulleys = [
    Pulley(Point(0, 0, size[2]), max_length, max_speed),
    Pulley(Point(size[0], 0, size[2]), max_length, max_speed),
    Pulley(Point(0, size[1], size[2]), max_length, max_speed),
    Pulley(Point(size[0], size[1], size[2]), max_length, max_speed),
]
space = Space(size[0], size[1], size[2], 0)

for p in pulleys:
    space.add_pulley(p)

start = Point(0, 0, 100)
end = Point(100, 100, 100)

space.update_lengths(start, -1, check_limit=False)
for p in space.pulleys:
    print(p.length)

len0 = []
len1 = []
len2 = []
len3 = []

point_count = 100
for i in range(point_count):
    x = (start.x + ((end.x - start.x) * i / point_count))
    y = (start.y + ((end.y - start.y) * i / point_count))
    z = (start.z + ((end.z - start.z) * i / point_count))
    target = Point(x, y, z)
    space.update_lengths(target, -1, check_limit=False)
    len0.append(space.pulleys[0].length)
    len1.append(space.pulleys[1].length)
    len2.append(space.pulleys[2].length)
    len3.append(space.pulleys[3].length)

import pyperclip

print(len0)
print(len1)
print(len2)
print(len3)

for len in [len0, len1, len2, len3]:
    pyperclip.copy("".join([f"{str(l).replace('.', ',')}\r\n" for l in len]))
    input("waiting...")
print("done")

plt.plot(len0)
plt.plot(len1)
plt.plot(len2)
plt.plot(len3)
plt.show()
