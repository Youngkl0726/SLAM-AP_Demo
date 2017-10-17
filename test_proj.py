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

class Len:
    def __init__(self, index, length):
        self.index = index
        self.length =length

bf = 40
fx = 672
fy = 672
cx = 393
cy = 220
invfx = 1.0 / fx
invfy = 1.0 / fy

# get R&t from file
def get_camera_traj(filename):
    camera_traj = [[] for i in range(360)]
    camera_file = open(filename)
    id = -1
    cnt = 0
    flag = 0
    num_r = 0
    line = ""
    for i in range(5836):
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


# get the coordinates of boxes from AP
def get_ap_info(filename):
    ap_file = open(filename)
    ap_num = -1
    ap_pos = [[] for i in range(360)]
    for i in range(463):
        ap_line = ap_file.readline()
        ap_line = ap_line.strip()
        if ap_line[0] == 's':
            ap_num = ap_num + 1
            # print ap_num
        else:
            ap_pos[ap_num].append(ap_line)
    ap_file.close()
    return ap_pos

# back projects a pixel into 3D world coordinates
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


# Visualize camera trajectory, AP boxes of cars and the trajectory of cars
def draw_points(camera_traj, ap_pos):
    sleep_t = 0.001
    color = ['red', 'brown', 'darkorange', 'darkmagenta', 'teal',
             'deepskyblue', 'royalblue', 'violet', 'purple', 'green', 'chocolate', 'black']
    cars = []
    lens = []
    color_id = 0
    x_p = []
    y_p = []
    pre_key = -1
    vvv = []
    idd = []
    # ori_y = 0.0
    for i in range(1):
        idd.append(i)
        print "i is : ", i
        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()

        # traj_car_img_dir = './sz_time/traj_car/'
        # traj_car_img_name = '{:0>6d}.png'.format(i)
        # traj_car_image_dir = path.join(traj_car_img_dir, traj_car_img_name)
        # traj_car_img = cv2.imread(traj_car_image_dir)
        # plt.axis('off')
        # plt.imshow(traj_car_img, cmap='gray')

        camera_t = camera_traj[i]
        camera = camera_t[0]
        r = [[] for k in range(3)]
        for k in range(3):
            for j in range(3):
                r[k].append(float(camera[j + k * 4]))
                # r[k].append(1.0)
        mat_r = np.mat(r)
        t = [[] for k in range(3)]
        for k in range(3):
            t[k].append(float(camera[3 + k * 4]))
        mat_t = np.mat(t)
        rwc = mat_r.transpose()
        ow = (-rwc).dot(mat_t)
        ow_list = ow.tolist()
        if i == 0:
            res = get_3d_wcor(358,287,72,rwc,ow)
            print "hehe"
            print res
        x_p.append(ow_list[0])
        y_p.append(ow_list[2])
        print "camera y is : ", ow_list[2]
        plt.axis([-5, 10, 0, 80])
        plt.scatter(x=x_p[i], y=y_p[i], marker='o')
        plt.plot(x_p[0:i], y_p[0:i])
        existing_ids = []

        for k in range(100, 300, 10):
            cor_res = get_3d_wcor(200, k, 10, rwc, ow)
            cor_x = cor_res[0][0]
            cor_y = cor_res[2][0]
            print cor_x, cor_y
            plt.scatter(x=cor_x, y=cor_y, c='black', marker='o')


    plt.show()

def main():
    camera_file = r'./sz_time/slamout_1002.txt'
    ap_file = r'./sz_time/ap1002.txt'
    camera_traj = get_camera_traj(camera_file)
    ap_pos = get_ap_info(ap_file)
    draw_points(camera_traj, ap_pos)


if __name__ == '__main__':
    main()
