from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
from PIL import Image
import numpy as np
import cv2

class Cars:

    def __init__(self, color, index, x, y):
        self.cor_x = []
        self.cor_y = []
        self.color = color
        self.index = index
        self.cor_x.append(x)
        self.cor_y.append(y)

bf = 379.8145
fx = 707.0912
fy = 707.0912
cx = 601.8873
cy = 183.1104
invfx = 1.0 / fx
invfy = 1.0 / fy

def get_ap_info(filename):
    ap_file = open(filename)
    ap_num = -1
    ap_pos = [[] for i in range(271)]
    for i in range(787):
        ap_line = ap_file.readline()
        ap_line = ap_line.strip()
        if ap_line[0] == 's':
            ap_num = ap_num + 1
            # print ap_num
        else:
            ap_pos[ap_num].append(ap_line)
    ap_file.close()
    return ap_pos

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


def get_camera_traj(filename):
    camera_file = open(filename)
    x_p = []
    y_p = []
    camera_traj = [[] for i in range(1801)]
    for i in range(271):
        camera_line = camera_file.readline()
        camera_line = camera_line.strip()
        camera_line = camera_line.split(" ")
        camera_traj[i].append(camera_line)
        x = float(camera_line[3])
        y = float(camera_line[11])
        x_p.append(x)
        y_p.append(y)
    camera_file.close()
    return camera_traj, x_p, y_p

camera_file = r'./Demo04/CameraTrajectory.txt'
camera_traj, camera_x, camera_y = get_camera_traj(camera_file)
ap_file = r'./Demo04/ap04.txt'
ap_pos = get_ap_info(ap_file)

for i in range(271):
    print i
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

    sleep_t = 0.001
    figure = plt.figure()
    plt.clf()
    plt.axis([-100, 300, -100, 600])
    plt.scatter(x=camera_x[i], y=camera_y[i], marker='o')
    ori_img_dir = './Demo04/image_0/'
    disp_img_dir = './kitti_disp_gen/04/'
    seg_img_dir = './Demo04/ideal_result/'
    image_name = '{:0>6d}.png'.format(i)
    ori_img = cv2.imread(path.join(ori_img_dir, image_name))
    disp_img = np.array(Image.open(path.join(disp_img_dir, image_name)))/256
    depth_img = bf / disp_img
    # print depth_img.max(), depth_img.min()
    # print depth_img.shape
    seg_img = np.array(Image.open(path.join(seg_img_dir, image_name)))

    cor_x = []
    cor_y = []
    for j in range(369, -1, -1):
        for k in range(1226):
            if seg_img[j][k] != 255:
                continue
            z = -(depth_img[j].max())
            # z = -depth_img[j][k]
            res = get_3d_wcor(j, k, z, rwc, ow)
            cor_x.append(-res[0][0])
            cor_y.append(-res[2][0])

    plt.scatter(x=cor_x[0:], y=cor_y[0:], c=[0.5, 0.5, 0.5], marker='o')

    # ap info
    cars = []
    existing_ids = []
    color = ['red', 'black', 'brown', 'darkorange', 'darkmagenta', 'teal',
             'deepskyblue', 'royalblue', 'violet', 'purple', 'green', 'chocolate']
    color_id = 0

    for line in (ap_pos[i]):
        line = line.split(' ')
        car_id = int(line[0])
        existing_ids.append(car_id)
        left = int(line[1])
        top = int(line[2])
        right = int(line[3])
        bottom = int(line[4])

        total_x = 0.0
        total_y = 0.0
        cnt = 0.0
        for u in range(top, bottom):
            for v in range(left, right):
                z = -depth_img[u][v]
                list_res = get_3d_wcor(u, v, z, rwc, ow)
                total_x -= list_res[0][0]
                total_y -= list_res[2][0]
                cnt += 1.0
        flag = 0

        for m in cars:
            index = m.index
            if index == car_id:
                flag = 1
                m.cor_x.append(total_x / cnt)
                m.cor_y.append(total_y / cnt)
                plt.plot(m.cor_x[0:], m.cor_y[0:], c=color[m.color])
                plt.scatter(x=m.cor_x[-1], y=m.cor_y[-1], c=color[m.color], marker='o')
                break
        if flag == 0:
            new_car = Cars(color_id, car_id, total_x / cnt, total_y / cnt)
            plt.scatter(x=new_car.cor_x[0:], y=new_car.cor_y[0:], c=color[new_car.color], marker='o')
            cars.append(new_car)
            color_id += 1
            color_id = color_id % 12

    plt.pause(sleep_t)
    print "ok"
plt.show()
