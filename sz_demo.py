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

bf = 96.768
fx = 672
fy = 672
cx = 393
cy = 220
invfx = 1.0 / fx
invfy = 1.0 / fy

# get R&t from file
def get_camera_traj(filename):
    camera_traj = [[] for i in range(620)]
    camera_file = open(filename)
    id = -1
    cnt = 0
    flag = 0
    num_r = 0
    line = ""
    for i in range(14870):
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
    ap_pos = [[] for i in range(620)]
    for i in range(2088):
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
    color_id = 0
    x_p = []
    y_p = []
    for i in range(620):
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
        x_p.append(ow_list[0])
        y_p.append(ow_list[2])
        plt.axis([-10, 10, 0, 150])
        plt.scatter(x=x_p[i], y=y_p[i], marker='o')
        plt.plot(x_p[0:i], y_p[0:i])
        existing_ids = []

        # Get depth map
        disp_img_dir = './sz_time/disp_0929_resize/'
        img_name = '{:0>6d}.png'.format(i)
        disp_image_dir = path.join(disp_img_dir, img_name)
        disp_img = np.array(Image.open(disp_image_dir))
        print disp_img
        # for u in range(456):
        #     for v in range(801):
        #         disp_img[u][v][0] = 1
                # if disp_img[u][v].any() == 0:
                #     disp_img[u][v][:] = 1
        disp_img = disp_img / 256
        depth_img = bf / disp_img
        # print img_depth
        # print np.max(img_depth), np.min(img_depth)

        # print "i is :", i, len(ap_pos[i])
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

            # vv = bottom
            # dep = 1.8 * fy / (cy -vv)
            # if dep < 0:
            #     dep = -1*dep
            # z = dep
            # list_res = get_3d_wcor(bottom, (left + right)/2, z, rwc, ow)
            # total_x = list_res[0][0]
            # total_y = list_res[2][0]
            # cnt = 1

            for u in range(top, bottom):
                for v in range(left, right):
                    z = depth_img[u][v]
                    # z = 50
                    print z
                    list_res = get_3d_wcor(u, v, z, rwc, ow)
                    total_x += list_res[0][0]
                    total_y += list_res[2][0]
                    cnt += 1.0
            if cnt == 0:
                continue
            flag = 0
            # print "cnt is: ", cnt
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

        for m in cars:
            flag = 0
            for n in existing_ids:
                if n == m.index:
                    flag = 1
            if flag == 0:
                cars.remove(m)
        # fig1.savefig('./sz_time/traj_car/{:0>6d}.png'.format(i))

        fig2 = plt.figure(2)
        plt.pause(sleep_t)
        plt.clf()

        file_dir = './sz_time/left_time/'
        image_name = '{:0>6d}.png'.format(i)
        img = mpimg.imread(path.join(file_dir, image_name))
        plt.axis([0, 801, 456, 0])
        plt.imshow(img, cmap='gray')

        ap_left = []
        ap_top = []
        ap_right = []
        ap_bottom = []
        for line in (ap_pos[i]):
            line = line.split(' ')
            left = float(line[1])
            top = float(line[2])
            right = float(line[3])
            bottom = float(line[4])
            ap_left.append(left)
            ap_top.append(top)
            ap_right.append(right)
            ap_bottom.append(bottom)
        ap_len = len(ap_top)
        for k in range(ap_len):
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

        fig3 = plt.figure(3)
        plt.axis([0, 801, 456, 0])
        plt.pause(sleep_t)
        plt.clf()
        disp_file_dir = r'./sz_time/disp_0929_resize/'
        disp_image_name = '{:0>6d}.png'.format(i)
        img = mpimg.imread(path.join(disp_file_dir, disp_image_name))
        plt.imshow(img, cmap='gray')

    plt.show()

def main():
    camera_file = r'./sz_time/slam_0929_2.txt'
    ap_file = r'./sz_time/ap0929.txt'
    camera_traj = get_camera_traj(camera_file)
    ap_pos = get_ap_info(ap_file)
    draw_points(camera_traj, ap_pos)


if __name__ == '__main__':
    main()
