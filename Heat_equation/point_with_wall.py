import time
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, ArtistAnimation
import imageio
import random
from PIL import Image
dt = 1
dx = 1
dy = 1
#k = 0.2

size = 100


def build_k_1(t, size): # постоянная температуропроводность
    n = t // dt
    k = np.array([[0.2] * size for i in range(size)])
    return k


def build_k_2(t, size): # непостоянная температуропроводность
    n = t // dt
    k = np.array([[0.25] * size for i in range(size)])
    for i in range(50):
        for j in range(size):
            k[i][j] = 0.05

    return k


def build_p_0(t, size, i, j): # точка-нагреватель
    n = t // dt
    p = np.zeros((n, size, size))
    for i1 in range(n):
        p[i1][i][j] = 1000

    return p


def build_p_1(t, size): # теплые капли на холодную поверхность
    n = t // dt
    p = np.zeros((n, size, size))
    for i in range(n):
        m = random.randint(1, 5)
        for j in range(m):
            i1 = random.randint(1, size - 1)
            j1 = random.randint(1, size - 1)
            for time in range(min(random.randint(20, 100), n - i - 1)):
                p[i + time][i1][j1] = 1000 #random.randint(0, 1500)

    return p


def build_p_2(t, size): # разные по температуре капли на холодную поверхность
    n = t // dt
    p = np.zeros((n, size, size))
    for i in range(n):
        m = random.randint(1, 5)
        for j in range(m):
            i1 = random.randint(1, size - 1)
            j1 = random.randint(1, size - 1)
            for time in range(min(random.randint(20, 100), n - i - 1)):
                p[i + time][i1][j1] = random.randint(0, 1500)

    return p



def update(t, size, p, k):
    n = t // dt
    temperature = np.zeros((n, size, size))
    for i in range(n):

        temperature[i] = temperature[i - dt]
        temperature[i] += dt * p[i]
        temperature[i] += k * (np.roll(temperature[i - dt], 1) + np.roll(temperature[i - dt], -1) - 2 * temperature[i - dt])
        temperature[i] += k * (np.transpose(np.roll(np.transpose(temperature[i - dt]), 1)) + np.transpose(np.roll(np.transpose(temperature[i - dt]), -1)) - 2 * temperature[i - dt])


        temperature[i][0] = 0
        temperature[i][size - 1] = 0
        for j in range(size):
            temperature[i][j][0] = 0
            temperature[i][j][size - 1] = 0
    return temperature

t = 1500
t += 1
k = np.array([[0.2] * size for i in range(size)])

k[60:100, 60:100] = 0.01


data = update(t, size, build_p_0(t, size, 55, 50), k)




def create_frame(t, data):
    global frames
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot([99, 60, 60], [60, 60, 99], color="grey")
    #ax.axhline(x=60, color="grey")
    cbar = ax.imshow(data[t], vmin=0, vmax=3000, cmap="hot")

    #ax.invert_yaxis()
    fig.colorbar(cbar)

    #plt.show()
    #ax.plot_trisurf(data[t], cmap='plasma', linewidth=0, antialiased=False)
    plt.title(f'Распространение тепла в момент {t}',
              fontsize=14)
    plt.savefig(f'/Users/kate/Desktop/img2/img_{t}.png',
                transparent = False,
                facecolor = 'white'
               )
    image = Image.open(f'/Users/kate/Desktop/img2/img_{t}.png')
    frames.append(image)
    plt.close()


frames = []
for t1 in range(0, t, 10):
    create_frame(t1, data)


imageio.mimsave('/Users/kate/Desktop/гифка/point_with_wall.gif', # output gif
                frames,          # array of input frames
                duration=0.001)

plt.show()
