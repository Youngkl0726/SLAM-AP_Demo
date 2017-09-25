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


def get_camera_traj(filename):
    camera_file = open(filename)
    x_p = []
    y_p = []
    camera_traj = [[] for i in range(500)]
    for i in range(500):
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

# get the coordinates of boxes from AP
def get_ap_info(filename):
    ap_file = open(filename)
    ap_num = -1
    ap_pos = [[] for i in range(500)]
    for i in range(1523):
        ap_line = ap_file.readline()
        ap_line = ap_line.strip()
        if ap_line[0] == 's':
            ap_num = ap_num + 1
            # print ap_num
        else:
            ap_pos[ap_num].append(ap_line)
    ap_file.close()
    return ap_pos

# get the coordinates of MapPoints in the picture and 3D world coordinate
def get_slam_info(filename):
    slam = open(filename)
    slam_3d_pos = [[] for i in range(500)]
    slam_pic_pos = [[] for i in range(500)]
    slam_num = -1
    for i in range(29278):
        slam_line = slam.readline()
        slam_line = slam_line.strip()
        # print slam_line
        if slam_line[0] == 'T':
            slam_num = slam_num + 1
            # print slam_num
            continue
        if slam_line[0] == '(':
            slam_pic_pos[slam_num].append(slam_line[1:-1])
        else:
            slam_3d_pos[slam_num].append(slam_line)
    slam.close()
    return slam_pic_pos, slam_3d_pos

def draw_points(x_p, y_p, slam_pic_pos, slam_3d_pos, ap_pos):
    sleep_t = 0.001
    color = ['red', 'brown', 'darkorange', 'darkmagenta', 'teal',
             'deepskyblue', 'royalblue', 'violet', 'purple', 'green', 'chocolate', 'black']
    cars = []
    color_id = 0
    for i in range(500):
        if i == 0:
            continue
        pic_x = []
        pic_y = []
        for line in (slam_pic_pos[i]):
            line = line.split(' ')
            x = float(line[0])
            y = float(line[1])
            pic_x.append(x)
            pic_y.append(y)

        point_x = []
        point_y = []
        for line in (slam_3d_pos[i]):
            line = line.split(' ')
            # print 'line[0] is : ', line[0]
            x = float(line[0])
            y = float(line[1])
            point_x.append(x)
            point_y.append(y)

        slam_len = len(point_x)

        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()
        plt.axis([-50, 200, 0, 300])
        plt.scatter(x=x_p[i], y=y_p[i], marker='o')
        plt.plot(x_p[0:i], y_p[0:i])
        existing_ids = []
        for line in (ap_pos[i]):
            line = line.split(' ')
            car_id = int(line[0])
            existing_ids.append(car_id)
            left = float(line[1])
            top = float(line[2])
            right = float(line[3])
            bottom = float(line[4])

            cnt = 0.0
            total_x = 0.0
            total_y = 0.0
            for j in range(slam_len):
                x = pic_x[j]
                y = pic_y[j]
                if x - left > 0.0000001 and right - x > 0.0000001 and y - top > 0.0000001 and bottom - y > 0.0000001:
                    total_x += point_x[j]
                    total_y += point_y[j]
                    cnt += 1.0
            if cnt == 0.0:
                for m in cars:
                    if m.index == car_id:
                        plt.plot(m.cor_x[0:], m.cor_y[0:], c=color[m.color])
                continue

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


        for m in cars:
            flag = 0
            for n in existing_ids:
                if n == m.index:
                    flag = 1
            if flag == 0:
                cars.remove(m)

        fig2 = plt.figure(2)
        plt.axis([0, 800, 410, 0])
        plt.pause(sleep_t)
        plt.clf()

        file_dir = r'./sz_time/left_time/'
        image_name = '{:0>6d}.png'.format(i)
        img = mpimg.imread(path.join(file_dir, image_name))
        plt.imshow(img, cmap='gray')
        # plt.scatter(x=pic_x[0:], y=pic_y[0:], c='r', marker='o')

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
        color_id2 = 0
        for k in range(ap_len):
            left = ap_left[k]
            top = ap_top[k]
            right = ap_right[k]
            bottom = ap_bottom[k]
            cor_x = []
            cor_y = []
            for j in range(slam_len):
                x = pic_x[j]
                y = pic_y[j]
                if x-left > 0.0000001 and right-x > 0.0000001 and y-top > 0.0000001 and bottom-y > 0.0000001:
                    cor_x.append(x)
                    cor_y.append(y)

            if len(cor_x) != 0:
                color_id2 += 1
                color_id2 = color_id2 % 12
                plt.scatter(x=cor_x[:], y=cor_y[:], c=color[color_id2], marker='o')
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
        plt.axis([0, 800, 410, 0])
        plt.pause(sleep_t)
        plt.clf()
        disp_file_dir = r'./sz_time/disp/'
        disp_image_name = '{:0>6d}.png'.format(i)
        img = mpimg.imread(path.join(disp_file_dir, disp_image_name))
        plt.imshow(img, cmap='gray')


    plt.show()


def main():
    camera_file = r'./sz_time/CameraTrajectory.txt'
    ap_file = r'./sz_time/aptime.txt'
    point_pos_file = r'./sz_time/sz_time_out.txt'
    camera_traj, camera_x, camera_y = get_camera_traj(camera_file)
    print len(camera_x)
    ap_pos = get_ap_info(ap_file)
    slam_pic_pos, slam_3d_pos = get_slam_info(point_pos_file)
    # draw_points(camera_traj, camera_x, camera_y, ap_pos)
    draw_points(camera_x, camera_y, slam_pic_pos, slam_3d_pos, ap_pos)

if __name__ == '__main__':
    main()
