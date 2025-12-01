import time
import numpy as np
from matplotlib import pyplot as plt
import random

dt = 1
dx = 1
dy = 1


def update(t, size, p, k):
    global start
    global finish
    global h
    n = t // dt
    temperature = np.zeros((n, size, size))

    t_down = -25
    t_up = 25
    temperature[0, 0: 50 + start + 1, 0:size] = t_down
    temperature[0, finish - 40:size, 0:size] = 0
    temperature[0, start + 130:finish, 0:size] = t_up

    for i in range(1, n):
        temperature[i] = temperature[i - dt]
        temperature[i] += dt * p[i]
        temperature[i] += k * (np.roll(temperature[i - dt], 1) + np.roll(temperature[i - dt], -1) - 2 * temperature[i - dt])
        temperature[i] += k * (np.transpose(np.roll(np.transpose(temperature[i - dt]), 1)) + np.transpose(np.roll(np.transpose(temperature[i - dt]), -1)) - 2 * temperature[i - dt])

        temperature[i, 0: 20 + start + 1, 0:size] = t_down
        temperature[i, finish - 20:size, 0:size] = t_up


    return temperature


size = 500
t = 15000
t += 1
start = 200
finish = 400
w = 10 # толщина стекла
h = 50 #высота первого стекла
d = 50
x = []
y = []

k = np.array([[0.2] * size for i in range(size)])
k[h + start:h + start + w + 1, 0:size] = 0.02  # стекло 1
k[h + start + w + d:h + start + 2 * w + d + 1, 0:size] = 0.02  # стекло 2
data = update(t, size, np.zeros((t, size, size)), k)




plt.ion()
for i in range(0, 1):
    plt.clf()
    start = 0
    finish = 0
    plt.axhline(y=h + start, color="grey")
    plt.axhline(y=h + start + w, color="grey")
    plt.axhline(y=h + start + w + d, color="grey")
    plt.axhline(y=h + start + 2 * w + d, color="grey")
    plt.text(10 + start, 10 + start, "Воздух", fontsize=10, fontfamily="serif")
    plt.text(10 + start, h + 7 + start, "Cтекло", fontsize=10, fontfamily="serif")
    plt.text(10 + start, h + 37 + start, "Воздушная прослойка", fontsize=10, fontfamily="serif")
    plt.text(10 + start, 117 + start, "Стекло", fontsize=10, fontfamily="serif")
    plt.text(10 + start, 145 + start, "Комната", fontsize=10, fontfamily="serif")


    pic = data[i, 200:400, 200:400]
    cbar = plt.imshow(pic, vmin=-30, vmax=30, cmap="cool")
    plt.title(f'Распространение тепла в момент {i}',
              fontsize=14)
    plt.colorbar(cbar)
    plt.gcf().canvas.flush_events()

    time.sleep(0.0001)
plt.ioff()

plt.show()


