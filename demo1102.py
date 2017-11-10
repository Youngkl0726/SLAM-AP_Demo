import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
from PIL import Image
import numpy as np
import cv2
import math
from scipy.optimize import curve_fit

class Cars:

    def __init__(self, color, index, x, y, picx, picy, depth, rwc, ow):
        self.cor_x = []
        self.cor_y = []
        self.pic_x = []
        self.pic_y = []
        self.rw = []
        self.o = []
        self.color = color
        self.index = index
        self.cor_x.append(x)
        self.cor_y.append(y)
        self.pic_x.append(picx)
        self.pic_y.append(picy)
        self.rw.append(rwc)
        self.o.append(ow)
        self.cnt = 1
        self.depth = depth

bf = 24
fx = 672
fy = 672
cx = 393
cy = 220
invfx = 1.0 / fx
invfy = 1.0 / fy

# get R&t from file
def get_camera_traj(filename):
    camera_traj = [[] for i in range(236)]
    camera_file = open(filename)
    id = -1
    cnt = 0
    flag = 0
    num_r = 0
    line = ""
    for i in range(4445):
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
            num_r = 1
    return camera_traj

def get_ap_log(filename):
    file = open(filename)
    res_line = [[] for i in xrange(117)]
    for i in xrange(117):
        # print i
        line = file.readline()
        line = line.strip()
        line = line.split(" ")
        # print len(line)
        # print line
        res_line[i].append(int(line[0]))
        res_line[i].append(int(line[1]))
        res_line[i].append(float(line[18]))
        res_line[i].append(float(line[19]))
        res_line[i].append(float(line[20]))
        res_line[i].append(float(line[21]))
        res_line[i].append(float(line[26]))
        res_line[i].append(float(line[27]))
        res_line[i].append(float(line[28]))
        res_line[i].append(float(line[29]))
        res_line[i].append(int(line[30]))
        res_line[i].append(int(line[31]))
        res_line[i].append(int(line[32]))
        res_line[i].append(int(line[33]))
    return res_line
        # print res_line[i]

# get the coordinates of boxes from AP
def get_ap_info(filename):
    ap_file = open(filename)
    ap_num = -1
    ap_pos = [[] for i in range(236)]
    for i in range(334):
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
    return list_res[0][0], list_res[2][0]

def rotate_point(x, y):
    a = math.atan2(2, 36)
    si = math.sin(a)
    co = math.cos(a)
    xx = x*co - y*si
    yy = y*co + x*si
    return xx, yy

def cal_depth(u, v):
    r = [7.21914340e+02, 2.27910142e+02, 3.54430380e-02]
    d = r[0] / (v - r[2] * u - r[1])
    return d

def f_2(x, a, b, c):
    y = a * x * x + b * x + c
    return y

# Visualize camera trajectory, AP boxes of cars and the trajectory of cars
# def draw_points1(camera_traj, ap_pos):
#     sleep_t = 0.001
#     color = ['red', 'brown', 'darkorange', 'darkmagenta', 'teal',
#              'deepskyblue', 'royalblue', 'violet', 'purple', 'green', 'chocolate', 'black']
#     cars = []
#     color_id = 0
#     x_p = []
#     y_p = []
#     for i in range(236):
#         # idd.append(i)
#         print "i is : ", i
#         fig1 = plt.figure(1)
#         plt.pause(sleep_t)
#         plt.clf()
#
#         # traj_car_img_dir = './sz_time/traj_car/'
#         # traj_car_img_name = '{:0>6d}.png'.format(i)
#         # traj_car_image_dir = path.join(traj_car_img_dir, traj_car_img_name)
#         # traj_car_img = cv2.imread(traj_car_image_dir)
#         # plt.axis('off')
#         # plt.imshow(traj_car_img, cmap='gray')
#
#         camera_t = camera_traj[i]
#         camera = camera_t[0]
#         r = [[] for k in range(3)]
#         for k in range(3):
#             for j in range(3):
#                 r[k].append(float(camera[j + k * 4]))
#         mat_r = np.mat(r)
#         t = [[] for k in range(3)]
#         for k in range(3):
#             t[k].append(float(camera[3 + k * 4]))
#         mat_t = np.mat(t)
#         rwc = mat_r.transpose()
#
#         ow = (-rwc).dot(mat_t)
#         ow_list = ow.tolist()
#
#         # Rotation
#         ow_list[0], ow_list[2] = rotate_point(ow_list[0][0], ow_list[2][0])
#         x_p.append(ow_list[0])
#         y_p.append(ow_list[2])
#         print "camera is : ", ow_list[0], ow_list[2]
#
#         plt.axis([-6, 6, 0, 40])
#         plt.scatter(x=x_p[i], y=y_p[i], marker='o')
#         plt.plot(x_p[0:i], y_p[0:i])
#         existing_ids = []
#
#         # Get depth map
#         disp_img_dir = './sz_time/disp_1103_resize/'
#         img_name = '{:0>6d}.png'.format(i)
#         disp_image_dir = path.join(disp_img_dir, img_name)
#         disp_img = np.array(Image.open(disp_image_dir))
#
#         disp_img = disp_img*1.0 / 256.0
#         for m in xrange(456):
#             for n in xrange(800):
#                 if disp_img[m][n] < 1.0:
#                     disp_img[m][n] = 1.0
#         depth_img = 32.0 * bf / disp_img
#         # print img_depth
#         # print np.max(depth_img), np.min(depth_img)
#
#         # print "i is :", i, len(ap_pos[i])
#
#         for line in (ap_pos[i]):
#             line = line.split(' ')
#             car_id = int(line[0])
#             existing_ids.append(car_id)
#             left = int(line[1])
#             top = int(line[2])
#             right = int(line[3])
#             bottom = int(line[4])
#
#             # if car_id != 4:
#             #     continue
#             flag_v = 1
#             ped_dep = []
#             depth_total = 0
#             depth_num = 0
#             for u in range(top, bottom):
#                 for v in range(left, right):
#                     d = depth_img[u][v]
#                     depth_total += d
#                     depth_num += 1
#                     ped_dep.append(d)
#             print "max/min is: ", max(ped_dep), min(ped_dep), depth_total/depth_num
#
#             # print "car_id is :", car_id
#             dep = cal_depth((left + right)/2, bottom)
#             print car_id, dep
#             z = dep
#
#             total_x = 0.0
#             total_y = 0.0
#             cnt = 0.0
#             total_x, total_y = get_3d_wcor(bottom, (left + right)/2, z, rwc, ow)
#             print "person y is : ", total_y
#             cnt = 1
#
#             if cnt == 0:
#                 continue
#             flag = 0
#             # print "cnt is: ", cnt
#             for m in cars:
#                 index = m.index
#                 # print "index is : ", index, "car_id is : ", car_id
#                 if index == car_id:
#                     flag = 1
#                     m.cor_x.append(total_x/cnt)
#                     m.cor_y.append(total_y/cnt)
#                     m.pic_x.append((left+right)/2)
#                     m.pic_y.append(bottom)
#                     m.rw.append(rwc)
#                     m.o.append(ow)
#                     m.cnt = m.cnt + 1
#                     if m.cnt > 2:
#                         print "fit!!!"
#                         r = curve_fit(f_2, m.pic_x, m.pic_y)[0]
#                         if len(r) > 0:
#                             for ind in xrange(len(m.pic_x)):
#                                 m.pic_y[ind] = r[0] * m.pic_x[ind] * m.pic_x[ind] + r[1] * m.pic_x[ind] + r[2]
#                                 m.cor_x[ind], m.cor_y[ind] = get_3d_wcor(m.pic_y[ind], m.pic_x[ind], m.depth, \
#                                                                          m.rw[ind], m.o[ind])
#                     plt.plot(m.cor_x[0:], m.cor_y[0:], c=color[m.color])
#                     plt.scatter(x=m.cor_x[-1], y=m.cor_y[-1], c=color[m.color], marker='o')
#                     break
#             if flag == 0:
#                 # print "flag = 0 car_id is: ", car_id
#                 new_car = Cars(color_id, car_id, total_x / cnt, total_y / cnt, (left+right)/2, bottom, dep, rwc, ow)
#                 plt.scatter(x=new_car.cor_x[0:], y=new_car.cor_y[0:], c=color[new_car.color], marker='o')
#                 cars.append(new_car)
#                 color_id += 1
#                 color_id = color_id % 12
#
#         for m in cars:
#             flag2 = 0
#             for n in existing_ids:
#                 if n == m.index:
#                     flag2 = 1
#             # if flag2 == 0:
#             #     cars.remove(m)
#         # fig1.savefig('./sz_time/traj_car/{:0>6d}.png'.format(i))
#
#         fig2 = plt.figure(2)
#         plt.pause(sleep_t)
#         plt.clf()
#
#         file_dir = './sz_time/ped1103/'
#         image_name = '{:0>6d}.png'.format(i)
#         img = mpimg.imread(path.join(file_dir, image_name))
#         plt.axis([0, 800, 456, 0])
#         plt.imshow(img, cmap='gray')
#
#         ap_left = []
#         ap_top = []
#         ap_right = []
#         ap_bottom = []
#         for line in (ap_pos[i]):
#             line = line.split(' ')
#             car_id = int(line[0])
#             left = float(line[1])
#             top = float(line[2])
#             right = float(line[3])
#             bottom = float(line[4])
#             ap_left.append(left)
#             ap_top.append(top)
#             ap_right.append(right)
#             ap_bottom.append(bottom)
#             for m in cars:
#                 index = m.index
#                 # print "index is : ", index, "car_id is : ", car_id
#                 if index == car_id:
#                     plt.plot(m.pic_x[0:], m.pic_y[0:], c=color[m.color])
#         ap_len = len(ap_top)
#         for k in range(ap_len):
#             left = ap_left[k]
#             top = ap_top[k]
#             right = ap_right[k]
#             bottom = ap_bottom[k]
#             p1 = []
#             p2 = []
#             p3 = []
#             p4 = []
#             p1.append(left)
#             p1.append(top)
#             p2.append(right)
#             p2.append(top)
#             p3.append(left)
#             p3.append(bottom)
#             p4.append(right)
#             p4.append(bottom)
#             plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c='green')
#             plt.plot([p1[0], p3[0]], [p1[1], p3[1]], c='green')
#             plt.plot([p4[0], p2[0]], [p4[1], p2[1]], c='green')
#             plt.plot([p4[0], p3[0]], [p4[1], p3[1]], c='green')
#
#     plt.show()

def draw_points2(camera_traj, ap_log):
    sleep_t = 0.001
    color = ['red', 'brown', 'darkorange', 'darkmagenta', 'teal',
             'deepskyblue', 'royalblue', 'violet', 'purple', 'green', 'chocolate', 'black']
    cars = []
    color_id = 0
    x_p = []
    y_p = []
    log_id = 0
    log_id2 = 0
    for i in range(236):
        # idd.append(i)
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
        mat_r = np.mat(r)
        t = [[] for k in range(3)]
        for k in range(3):
            t[k].append(float(camera[3 + k * 4]))
        mat_t = np.mat(t)
        rwc = mat_r.transpose()

        ow = (-rwc).dot(mat_t)
        ow_list = ow.tolist()

        # Rotation
        ow_list[0], ow_list[2] = rotate_point(ow_list[0][0], ow_list[2][0])
        x_p.append(ow_list[0])
        y_p.append(ow_list[2])
        print "camera is : ", ow_list[0], ow_list[2]

        plt.axis([-6, 6, 0, 50])
        plt.scatter(x=x_p[i], y=y_p[i], marker='o')
        plt.plot(x_p[0:i], y_p[0:i])
        existing_ids = []

        # print "i is :", i, len(ap_pos[i])

        while log_id < 117 and int(ap_log[log_id][0]) == i:
            # Get depth map
            disp_img_dir = './sz_time/disp_1103_resize/'
            img_name = '{:0>6d}.png'.format(i)
            disp_image_dir = path.join(disp_img_dir, img_name)
            disp_img = np.array(Image.open(disp_image_dir))

            disp_img = disp_img * 1.0 / 256.0
            for m in xrange(456):
                for n in xrange(800):
                    if disp_img[m][n] < 1.0:
                        disp_img[m][n] = 1.0
            depth_img = 32.0 * bf / disp_img
            # print img_depth
            # print np.max(depth_img), np.min(depth_img)

            car_id = ap_log[log_id][1]
            existing_ids.append(car_id)
            point1_x = ap_log[log_id][2]
            point1_y = ap_log[log_id][3]
            point2_x = ap_log[log_id][4]
            point2_y = ap_log[log_id][5]

            foot1_x = ap_log[log_id][6]
            foot1_y = ap_log[log_id][7]
            foot2_x = ap_log[log_id][8]
            foot2_y = ap_log[log_id][9]

            left = ap_log[log_id][10]
            top = ap_log[log_id][11]
            right = ap_log[log_id][12]
            bottom = ap_log[log_id][13]

            mid_x = int((point1_x+point2_x)/2)
            mid_y = int((point1_y + point2_y) / 2)
            foot_mid_x = int((foot1_x+foot2_x)/2)
            foot_mid_y = int((foot1_y + foot2_y)/2)

            z = depth_img[mid_y][mid_x]
            print "depth is :", car_id, z

            total_x, total_y = get_3d_wcor(foot_mid_y, foot_mid_x, z, rwc, ow)
            print "person y is : ", total_y
            cnt = 1
            flag = 0
            # print "cnt is: ", cnt
            for m in cars:
                index = m.index
                # print "index is : ", index, "car_id is : ", car_id
                if index == car_id:
                    flag = 1
                    m.cor_x.append(total_x / cnt)
                    m.cor_y.append(total_y / cnt)
                    m.pic_x.append(foot_mid_x)
                    m.pic_y.append(foot_mid_y)
                    m.rw.append(rwc)
                    m.o.append(ow)
                    m.cnt = m.cnt + 1
                    if m.cnt > 2:
                        print "fit!!!"
                        r = curve_fit(f_2, m.pic_x, m.pic_y)[0]
                        if len(r) > 0:
                            for ind in xrange(len(m.pic_x)):
                                m.pic_y[ind] = r[0] * m.pic_x[ind] * m.pic_x[ind] + r[1] * m.pic_x[ind] + r[2]
                                m.cor_x[ind], m.cor_y[ind] = get_3d_wcor(m.pic_y[ind], m.pic_x[ind], m.depth, m.rw[ind], m.o[ind])
                    plt.plot(m.cor_x[0:], m.cor_y[0:], c=color[m.color])
                    plt.scatter(x=m.cor_x[-1], y=m.cor_y[-1], c=color[m.color], marker='o')
                    break
            if flag == 0:
                # print "flag = 0 car_id is: ", car_id
                new_car = Cars(color_id, car_id, total_x / cnt, total_y / cnt, (left + right) / 2, bottom, z, rwc, ow)
                plt.scatter(x=new_car.cor_x[0:], y=new_car.cor_y[0:], c=color[new_car.color], marker='o')
                cars.append(new_car)
                color_id += 1
                color_id = color_id % 12
            if log_id+1 < 117 and ap_log[log_id+1][0] == i:
                log_id += 1
            else:
                log_id += 1
                break

        fig2 = plt.figure(2)
        plt.pause(sleep_t)
        plt.clf()

        file_dir = './sz_time/ped1103/'
        image_name = '{:0>6d}.png'.format(i)
        img = mpimg.imread(path.join(file_dir, image_name))
        plt.axis([0, 800, 456, 0])
        plt.imshow(img, cmap='gray')

        ap_left = []
        ap_top = []
        ap_right = []
        ap_bottom = []

        while log_id2 < 117 and ap_log[log_id2][0] == i:
            left = ap_log[log_id2][10]
            top = ap_log[log_id2][11]
            right = ap_log[log_id2][12]
            bottom = ap_log[log_id2][13]
            ap_left.append(left)
            ap_top.append(top)
            ap_right.append(right)
            ap_bottom.append(bottom)

            if log_id2+1 < 117 and ap_log[log_id2+1][0] == i:
                log_id2 += 1
            else:
                log_id2 += 1
                break
        ap_len = len(ap_top)
        print ap_len
        for k in xrange(ap_len):
            left = ap_left[k]
            top = ap_top[k]
            right = ap_right[k]
            bottom = ap_bottom[k]
            p1 = []
            p2 = []
            p3 = []
            p4 = []
            p1.append(left)
            p1.append(top)
            p2.append(right)
            p2.append(top)
            p3.append(left)
            p3.append(bottom)
            p4.append(right)
            p4.append(bottom)
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c='green')
            plt.plot([p1[0], p3[0]], [p1[1], p3[1]], c='green')
            plt.plot([p4[0], p2[0]], [p4[1], p2[1]], c='green')
            plt.plot([p4[0], p3[0]], [p4[1], p3[1]], c='green')
    plt.show()

def main():
    ap_log = get_ap_log(r'./sz_time/r_demo0_l_out.log')
    camera_file = r'./sz_time/ped_1103.txt'
    ap_file = r'./sz_time/ap_1103.txt'
    camera_traj = get_camera_traj(camera_file)
    ap_pos = get_ap_info(ap_file)
    # draw_points1(camera_traj, ap_pos)
    draw_points2(camera_traj, ap_log)


if __name__ == '__main__':
    main()
