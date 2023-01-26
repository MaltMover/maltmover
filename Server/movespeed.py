import pandas as pd
import matplotlib.pyplot as plt
import pyperclip

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
space = Space(size[0], size[1], size[2], edge_limit=0)

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
sums = []
for i in range(point_count+1):
    x = (start.x + ((end.x - start.x) * i / point_count))
    y = (start.y + ((end.y - start.y) * i / point_count))
    z = (start.z + ((end.z - start.z) * i / point_count))
    target = Point(x, y, z)
    space.update_lengths(target, -1, check_limit=False)
    len0.append(space.pulleys[0].length)
    len1.append(space.pulleys[1].length)
    len2.append(space.pulleys[2].length)
    len3.append(space.pulleys[3].length)


lens = [len0, len1, len2, len3]
rows = []

for i in range(len(len0)):
    row = []
    for length in lens:
        row.append(str(length[i]).replace(".", ","))
    rows.append(row)

rows = ["\t".join(row) for row in rows]
table = "\r\n".join(rows)
pyperclip.copy(table)

print(sums)
plt.plot(len0)
plt.plot(len1)
plt.plot(len2)
plt.plot(len3)
plt.show()
