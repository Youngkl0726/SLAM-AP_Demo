import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
from PIL import Image
import numpy as np
import cv2

bf = 40
fx = 672
fy = 672
cx = 393
cy = 220
invfx = 1.0 / fx
invfy = 1.0 / fy

# get R&t from file
def get_camera_traj(filename):
    camera_traj = [[] for i in range(435)]
    camera_file = open(filename)
    id = -1
    cnt = 0
    flag = 0
    num_r = 0
    line = ""
    for i in range(32960):
        camera_line = camera_file.readline()
        camera_line = camera_line.strip()
        li = camera_line.split(" ")
        # print camera_line[0]
        if camera_line[0] == 'T':
            id += 1
            num_r = 0
            if flag == 1:
                camera_traj[id].append(camera_traj[id-1][0])
        if camera_line[0] == 'R':
            if num_r == 1:
                continue
            flag = 1
            if id != 0:
                camera_traj[id].pop()
            # print camera_line
            camera_line = camera_line.split(" ")
            # print camera_line
            camera_traj[id].append(camera_line[1:])
            x = float(li[3])
            y = float(li[11])
            num_r = 1
    return camera_traj

def get_3d_wcor(u, v, z, rwc, ow):
    x = (v - cx) * z * invfx
    y = (u - cy) * z * invfy
    x3dc = [[] for k in range(3)]
    x3dc[0].append(x)
    x3dc[1].append(y)
    x3dc[2].append(z)
    mat_3dc = np.mat(x3dc)
    mat_res = rwc.dot(mat_3dc) + ow
    # print mat_res[0][0], mat_res[2][0]
    list_res = mat_res.tolist()
    return list_res

def draw_points(camera_traj):
    sleep_t = 0.001
    x_p = []
    y_p = []
    for i in range(435):
        # idd.append(i)
        print "i is : ", i
        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()

        camera_t = camera_traj[i]
        camera = camera_t[0]
        r = [[] for k in range(3)]
        for k in range(3):
            for j in range(3):
                r[k].append(float(camera[j + k * 4]))
        mat_r = np.mat(r)
        t = [[] for k in range(3)]
        for k in range(3):
            t[k].append(float(camera[3 + k * 4]))
        mat_t = np.mat(t)
        rwc = mat_r.transpose()

        ow = (-rwc).dot(mat_t)
        ow_list = ow.tolist()
        print rwc, ow_list
        x_p.append(ow_list[0])
        y_p.append(ow_list[2])
        plt.axis([-10, 5, 0, 20])
        print x_p[i][0], y_p[i][0]
        plt.scatter(x=x_p[i][0], y=y_p[i][0], marker='o')
        plt.plot(x_p[0:i], y_p[0:i])

    plt.show()

def main():
    camera_file = r'./light/light_15.txt'

    camera_traj = get_camera_traj(camera_file)

    draw_points(camera_traj)


if __name__ == '__main__':
    main()
