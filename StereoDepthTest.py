import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
import numpy as np
from PIL import Image

def get_ap_log(filename):
    file = open(filename)
    res_line = [[] for i in xrange(471)]
    for i in xrange(471):
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
    # print res_line
    return res_line

bf = 200.0

def draw(ap_res):
    depth = []
    depth_id = []
    depth_num = 0
    sleep_t = 0.001
    for i in range(471):
        # print ap_res[i]
        # Get depth map
        person_id = ap_res[i][1]
        if (person_id != 12) and (person_id != 80) and (person_id != 96) :
            continue
        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()
        pic_id = ap_res[i][0]
        disp_img_dir = './Stereo/test_1215_disp_resize/'
        img_name = '{:0>6d}.png'.format(pic_id)
        disp_image_dir = path.join(disp_img_dir, img_name)
        disp_img = np.array(Image.open(disp_image_dir))

        disp_img = disp_img * 1.0 / 8.0
        for m in xrange(1101):
            for n in xrange(1857):
                if disp_img[m][n] < 0.3:
                    disp_img[m][n] = 0.3
        depth_img = 32.0 * bf / disp_img
        point1_x = ap_res[i][2]
        point1_y = ap_res[i][3]
        point2_x = ap_res[i][4]
        point2_y = ap_res[i][5]
        mid_x = int((point1_x + point2_x) / 2)
        mid_y = int((point1_y + point2_y) / 2)
        mid_x = min(1857, mid_x)
        mid_y = min(1101, mid_y)
        print disp_img[mid_y][mid_x]
        z = depth_img[mid_y][mid_x]
        depth.append(z)
        depth_id.append(depth_num)
        depth_num += 1
        plt.axis([0, 80, 0, 20])
        plt.plot(depth_id[0:], depth[0:], c='blue')
    plt.pause(10)
    plt.show()

def main():
    ap_file = r'./Stereo/r_l_out.log'
    ap_res = get_ap_log(ap_file)
    draw(ap_res)


if __name__ == '__main__':
    main()
