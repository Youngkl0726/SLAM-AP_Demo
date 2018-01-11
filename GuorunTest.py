import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
import numpy as np
from PIL import Image

def get_ap_log(filename):
    file = open(filename)
    txt_file = open('ap.txt', 'wb')
    num = 0
    frame_id = 0
    for i in xrange(19141):
    # for i in xrange(10):
        print i
        line = file.readline()
        line = line.strip()
        line = line.split(" ")
        # print line
        if len(line) == 2:
            frame_id = line[1]
            # print "frame_id is : ", frame_id
        if len(line) > 2:
            # print line[5]
            line1 = line[5].split(',')
            # print frame_id, line[0], line1
            # print line1
            # print len(line1)
            txt_file.write(frame_id+' '+line[0])
            for j in xrange(28):
                txt_file.write(' '+line1[j])
            txt_file.write('\n')
    txt_file.close()

def get_ap_log1(filename):
    file = open(filename)
    res_line = [[] for i in xrange(7558)]
    for i in xrange(7558):
        # print i
        line = file.readline()
        line = line.strip()
        line = line.split(" ")
        # print len(line)
        # print line
        res_line[i].append(int(line[0]))
        res_line[i].append(int(line[1]))
        res_line[i].append(float(line[6]))
        res_line[i].append(float(line[7]))
        res_line[i].append(float(line[8]))
        res_line[i].append(float(line[9]))
    # print res_line
    return res_line

bf = 500

def get_disp(ap_res):
    depth = []
    disp = []
    id = []
    sleep_t = 0.001
    num = 0
    for i in xrange(7558):
        person_id = ap_res[i][1]
        pic_id = ap_res[i][0]
        if pic_id < 3350 or pic_id > 3525:
            continue
        # print "person_id is: ", person_id
        if person_id != 24:
            continue
        num += 1
        print num
        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()
        pic_id = ap_res[i][0]
        disp_img_dir = './disp/'
        img_name = '{:0>6d}.png'.format(pic_id)
        disp_image_dir = path.join(disp_img_dir, img_name)
        disp_img = np.array(Image.open(disp_image_dir))
        disp_img = disp_img * 1.0 / 256.0
        depth_img = bf / disp_img
        point1_x = ap_res[i][2]
        point1_y = ap_res[i][3]
        point2_x = ap_res[i][4]
        point2_y = ap_res[i][5]
        mid_x = int((point1_x + point2_x) / 2)
        mid_y = int((point1_y + point2_y) / 2)
        mid_x = min(1847, mid_x)
        mid_y = min(1078, mid_y)
        disp.append(disp_img[mid_y][mid_x])
        z = depth_img[mid_y][mid_x]
        depth.append(z)
        id.append(num)
        plt.axis([0, 160, 35, 100])
        # plt.plot(id[0:], disp[0:], c='blue')
        plt.plot(id[0:], depth[0:], c='blue')
    plt.pause(10)
    plt.show()

def main():
    # ap_file = r'./disp/AP.txt'
    # get_ap_log(ap_file)
    ap_res = get_ap_log1('ap.txt')
    get_disp(ap_res)

if __name__ == '__main__':
    main()