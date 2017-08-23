import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path

# get camera trajectory
def get_camera_traj(filename):
    camera_file = open(filename)
    x_p = []
    y_p = []
    for i in range(1801):
        camera_line = camera_file.readline()
        camera_line = camera_line.strip()
        camera_line = camera_line.split(" ")
        x = float(camera_line[3])
        y = float(camera_line[11])
        x_p.append(x)
        y_p.append(y)
    camera_file.close()
    return x_p, y_p

# get the coordinates of MapPoints in the picture and 3D world coordinate
def get_slam_info(filename):
    slam = open(filename)
    slam_3d_pos = [[] for i in range(1801)]
    slam_pic_pos = [[] for i in range(1801)]
    slam_num = -1
    for i in range(414764):
        slam_line = slam.readline()
        slam_line = slam_line.strip()
        # print slam_line
        if slam_line[0] == 'T':
            slam_num = slam_num + 1
            # print slam_num
            continue
        if slam_line[0] == 'C':
            continue
        if slam_line[0] == '(':
            slam_pic_pos[slam_num].append(slam_line[1:-1])
        else:
            slam_3d_pos[slam_num].append(slam_line)
    slam.close()
    return slam_pic_pos, slam_3d_pos

# get the coordinates of boxes from AP
def get_ap_info(filename):
    ap_file = open(filename)
    ap_num = -1
    ap_pos = [[] for i in range(1801)]
    for i in range(9538):
        ap_line = ap_file.readline()
        ap_line = ap_line.strip()
        if ap_line[0] == 's':
            ap_num = ap_num + 1
            # print ap_num
        else:
            ap_pos[ap_num].append(ap_line)
    ap_file.close()
    return ap_pos

# visualize camera trajectory, MapPoints in pictures and AP boxes of cars
def draw_points(x_p, y_p, slam_pic_pos, slam_3d_pos, ap_pos):
    sleep_t = 0.001
    for i in range(1801):
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
            x = float(line[0])
            y = float(line[1])
            point_x.append(x)
            point_y.append(y)

        slam_len = len(point_x)

        color = ['red', 'yellow', 'pink', 'brown', 'chocolate', 'darkorange', 'burlywood', 'cyan',
                 'deepskyblue', 'royalblue', 'violet', 'purple', 'green']
        # print len(color)
        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()
        plt.axis([-100, 300, 0, 400])
        plt.plot(x_p[0:i], y_p[0:i], c='black')
        if len(ap_pos[i]) != 0:
            map_point_x = []
            map_point_y = []
            for line in (ap_pos[i]):
                line = line.split(' ')
                left = float(line[0])
                top = float(line[1])
                right = float(line[2])
                bottom = float(line[3])
                cnt = 0.0
                total_x = 0.0
                total_y = 0.0
                for j in range(slam_len):
                    x = pic_x[j]
                    y = pic_y[j]
                    if x-left>0.0000001 and right-x>0.0000001 and y-top>0.0000001 and bottom-y>0.0000001:
                        # map_point_x.append(point_x[j])
                        # map_point_y.append(point_y[j])
                        # break
                        total_x += point_x[j]
                        total_y += point_y[j]
                        cnt += 1.0

                # print cnt
                if cnt == 0.0:
                    continue
                map_point_x.append(total_x/cnt)
                map_point_y.append(total_y/cnt)
            # print len(map_point_x)
            for j in range(len(map_point_x)):
                print map_point_x[j], map_point_y[j]
                plt.scatter(x=map_point_x[j], y=map_point_y[j], c=color[j], marker='o')
        # plt.scatter(x=point_x[0:], y=point_y[0:], c='r', marker='o')

        fig2 = plt.figure(2)
        plt.axis([0, 1250, 350, 0])
        plt.pause(sleep_t)
        plt.clf()

        file_dir = '/Users/youngkl/Desktop/Demo/image_0/'
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
            left = float(line[0])
            top = float(line[1])
            right = float(line[2])
            bottom = float(line[3])
            ap_left.append(left)
            ap_top.append(top)
            ap_right.append(right)
            ap_bottom.append(bottom)
        ap_len = len(ap_top)
        color_id = 0
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
                if x-left>0.0000001 and right-x>0.0000001 and y-top>0.0000001 and bottom-y>0.0000001:
                    cor_x.append(x)
                    cor_y.append(y)

            if len(cor_x) != 0:
                color_id += 1
                plt.scatter(x=cor_x[:], y=cor_y[:], c=color[color_id], marker='o')
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
    camera_file = r'CameraTrajectory.txt'
    slam2 = r'slam_out2.txt'
    ap_file = r'ap_out.txt'
    camera_x, camera_y = get_camera_traj(camera_file)
    print len(camera_x)
    slam_pic_pos, slam_3d_pos = get_slam_info(slam2)
    ap_pos = get_ap_info(ap_file)
    draw_points(camera_x, camera_y, slam_pic_pos, slam_3d_pos, ap_pos)


if __name__ == '__main__':
    main()
