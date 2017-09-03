import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
from PIL import Image
import numpy as np

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

# get camera trajectory
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

# get the coordinates of boxes from AP
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

# Visualize camera trajectory, MapPoints in pictures and AP boxes of cars
def draw_points(camera_traj, x_p, y_p, ap_pos):
    sleep_t = 0.001
    color = ['red', 'black', 'brown', 'darkorange', 'darkmagenta', 'teal',
             'deepskyblue', 'royalblue', 'violet', 'purple', 'green', 'chocolate']
    cars = []
    color_id = 0
    for i in range(271):
        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()
        plt.axis([-100, 300, -100, 500])
        plt.plot(x_p[0:i], y_p[0:i])
        existing_ids = []
        camera_t = camera_traj[i]
        camera = camera_t[0]

        # print camera
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
        # print mat_r
        # print mat_t
        ow = (-rwc).dot(mat_t)
        # print rwc.dot(mat_t)
        # print ow
        print "i is :", i, len(ap_pos[i])
        for line in (ap_pos[i]):
            line = line.split(' ')
            car_id = int(line[0])
            existing_ids.append(car_id)
            left = int(line[1])
            top = int(line[2])
            right = int(line[3])
            bottom = int(line[4])

            img_dir = '/Users/youngkl/Desktop/Demo/kitti_disp_gen/04/'
            img_name = '{:0>6d}.png'.format(i)
            image_dir = path.join(img_dir, img_name)
            img = np.array(Image.open(image_dir))
            img = img/256
            img_depth = bf/img
            # print img_depth
            # print np.max(img_depth), np.min(img_depth)
            total_x = 0.0
            total_y = 0.0
            cnt = 0.0
            for u in range(top, bottom):
                for v in range(left, right):
                    z = -img_depth[u][v]
                    x = (v-cx)*z*invfx
                    y = (u-cy)*z*invfy
                    x3dc = [[] for k in range(3)]
                    x3dc[0].append(x)
                    x3dc[1].append(y)
                    x3dc[2].append(z)
                    mat_3dc = np.mat(x3dc)
                    mat_res = rwc.dot(mat_3dc) + ow
                    # print mat_res[0][0], mat_res[2][0]
                    list_res = mat_res.tolist()
                    # print list_res
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
        plt.axis([0, 1250, 350, 0])
        plt.pause(sleep_t)
        plt.clf()

        file_dir = '/Users/youngkl/Desktop/Demo/Demo04/image_0/'
        image_name = '{:0>6d}.png'.format(i)
        img = mpimg.imread(path.join(file_dir, image_name))
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

    plt.show()

def main():
    camera_file = r'./Demo04/CameraTrajectory.txt'
    ap_file = r'./Demo04/ap04.txt'
    camera_traj, camera_x, camera_y = get_camera_traj(camera_file)
    print len(camera_x)
    ap_pos = get_ap_info(ap_file)
    draw_points(camera_traj, camera_x, camera_y, ap_pos)


if __name__ == '__main__':
    main()
