import pandas as pd
import numpy
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
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

start = Point(10, 20, 100)
end = Point(90, 30, 100)

space.move_grabber(start, -1, check_limit=False)
for p in space.pulleys:
    print(p.length)

len0 = []
len1 = []
len2 = []
len3 = []

point_count = 100
sums = []
for i in range(point_count + 1):
    x = (start.x + ((end.x - start.x) * i / point_count))
    y = (start.y + ((end.y - start.y) * i / point_count))
    z = (start.z + ((end.z - start.z) * i / point_count))
    target = Point(x, y, z)
    space.move_grabber(target, -1, check_limit=False)
    len0.append(space.pulleys[0].length)
    len1.append(space.pulleys[1].length)
    len2.append(space.pulleys[2].length)
    len3.append(space.pulleys[3].length)

lens = [len0, len1, len2, len3]
rows = []
# x = list(range(len(len0)))
# y = len2
# print(len2)
# model = numpy.poly1d(numpy.polyfit(x, y, 2))
# a = float(model[2])
# b = float(model[1])
# c = float(model[0])
# c = float(len2[0])
# r2 = r2_score(y, model(x))
# print(a, b, c)
# print(r2)
# line = numpy.linspace(0, len(len0), 100)
# plt.plot(numpy.polyval(model, line))
# plt.show()

for i in range(len(len0)):
    row = []
    for length in lens:
        row.append(str(length[i]).replace(".", ","))
    rows.append(row)

rows = ["\t".join(row) for row in rows]
table = "\r\n".join(rows)
pyperclip.copy(table)

# print(sums)
plt.plot(len0)
plt.plot(len1)
plt.plot(len2)
plt.plot(len3)
plt.show()


# create the training data
x = [[int(i)] for i in range(len(len2))]
print(x)
y = len2

# transform the data to include polynomial features
poly = PolynomialFeatures(degree=2)
x_poly = poly.fit_transform(x)

# create and fit the model with specified y-intercept
model = LinearRegression(fit_intercept=True)
model.fit(x_poly, y)
model.intercept_ = len2[0]  # specify y-intercept

print(model.coef_)
# predict new values
x_new = [[100]]
y_new = model.predict(poly.transform(x_new))
print(y_new)
