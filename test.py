import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
from PIL import Image
import numpy as np
import cv2

def get_camera_traj(filename):
    camera_file = open(filename)
    x_p = []
    y_p = []
    camera_traj = [[] for i in range(1801)]
    for i in range(70):
        camera_line = camera_file.readline()
        camera_line = camera_line.strip()
        camera_line = camera_line.split(" ")
        camera_traj[i].append(camera_line)
        x = float(camera_line[3])
        y = float(camera_line[11])
        x_p.append(x)
        y_p.append(y)
    camera_file.close()
    return x_p, y_p

camera_file = r'CameraTrajectory2.txt'
camera_x, camera_y = get_camera_traj(camera_file)
print len(camera_x)
sleep_t = 0.001
for i in range(70):
    fig1 = plt.figure(1)
    plt.pause(sleep_t)
    plt.clf()
    plt.axis([-150, 100, 0, 450])
    # plt.scatter(x=camera_x[i], y=camera_y[i], marker='o')
    plt.plot(camera_x[0:i], camera_y[0:i])
plt.show()
