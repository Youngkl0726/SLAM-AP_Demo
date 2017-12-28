import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os import path
import numpy as np
from PIL import Image

def get_ap_log(filename):
    file = open(filename)
    res_line = [[] for i in xrange(4544)]
    for i in xrange(4543):
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

def get_ap_log1(filename):
    file = open(filename)
    res_line = [[] for i in xrange(4552)]
    for i in xrange(4552):
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

bf = 350
# bf = 100.0
def draw(ap_res):
    depth = []
    depth_id = []
    depth_num = 0
    point_xcord = []
    point_ycord = []
    point_num = 0
    sleep_t = 0.001
    num = 0
    disp = [[] for i in xrange(236)]
    # disp = []
    x = 0.0
    for i in range(493):
        # if i < 959 or i > 1354:
        #     continue

        person_id = ap_res[i][1]
        if person_id != 0:
            continue
        num += 1
        # fig1 = plt.figure(1)
        # plt.pause(sleep_t)
        # plt.clf()
        pic_id = ap_res[i][0]
        disp_img_dir = './Stereo/test_1215_kitti_disp_resize/'
        img_name = '{:0>6d}.png'.format(pic_id)
        disp_image_dir = path.join(disp_img_dir, img_name)
        disp_img = np.array(Image.open(disp_image_dir))

        disp_img = disp_img * 1.0 / 16.0
        # for m in xrange(1083):
        #     for n in xrange(1834):
        #         if disp_img[m][n] < 0.3:
        #             disp_img[m][n] = 0.3
        depth_img = 16.0 * bf / disp_img
        point1_x = ap_res[i][2]
        point1_y = ap_res[i][3]
        point2_x = ap_res[i][4]
        point2_y = ap_res[i][5]
        mid_x = int((point1_x + point2_x) / 2)
        mid_y = int((point1_y + point2_y) / 2)
        mid_x = min(1846, mid_x)
        mid_y = min(1083, mid_y)
        point_xcord.append(mid_x)
        point_ycord.append(mid_y)
        point_num += 1
        # print pic_id, "(", mid_y, mid_x, ")", disp_img[mid_y][mid_x]/16.0

        disp[num-1].append(pic_id)
        disp[num-1].append(disp_img[mid_y][mid_x]/16.0)

        # disp.append(disp_img[mid_y][mid_x] * 1.0 / 16.0)

        # print disp_img[mid_y][mid_x]*1.0/16.0
        x += disp_img[mid_y][mid_x]*1.0/16.0

        z = depth_img[mid_y][mid_x]
        depth.append(z)
        depth_id.append(depth_num)
        depth_num += 1
        # plt.axis([0, 200, 0, 40])
        # plt.plot(depth_id[0:], depth[0:], c='blue')

        # fig2 = plt.figure(2)
        # # plt.axis([0, 1250, 350, 0])
        # plt.pause(sleep_t)
        # plt.clf()
        # file_dir = './Stereo/test1215/'
        # image_name = '{:0>6d}.png'.format(pic_id)
        # img = mpimg.imread(path.join(file_dir, image_name))
        # plt.imshow(img, cmap='gray')
        # plt.plot(point_xcord[0:], point_ycord[0:], c='r')
    print "average disp2: ", x/(num*1.0)
    print num
    return disp
    # plt.pause(10)
    # plt.show()

def get_disp(ap_res, ap_res1):
    num = 0
    x = 0.0
    disp = [[] for i in xrange(233)]
    # disp = []
    for i in range(493):
        # if i < 959 or i > 1354:
        #     continue
        person_id = ap_res[i][1]
        pic_id = ap_res[i][0]

        if person_id != 0:
            continue
        point1_x = ap_res[i][2]
        point1_y = ap_res[i][3]
        point2_x = ap_res[i][4]
        point2_y = ap_res[i][5]
        mid_x = int((point1_x + point2_x) / 2)
        mid_y = int((point1_y + point2_y) / 2)
        mid_x = min(1846, mid_x)
        mid_y = min(1083, mid_y)
        for j in range(494):
            person_id1 = ap_res1[j][1]
            pic_id1 = ap_res1[j][0]
            if pic_id == pic_id1 and person_id == 0 and 0 == person_id1:
                point1_x1 = ap_res1[j][2]
                point1_y1 = ap_res1[j][3]
                point2_x1 = ap_res1[j][4]
                point2_y1 = ap_res1[j][5]
                mid_x1 = int((point1_x1 + point2_x1) / 2)
                mid_y1 = int((point1_y1 + point2_y1) / 2)
                mid_x1 = min(1846, mid_x1)
                mid_y1 = min(1083, mid_y1)
                # print mid_x, mid_x1, abs(mid_x-mid_x1)
                disp[num].append(pic_id)
                disp[num].append(abs(mid_x-mid_x1))

                # disp.append(abs(mid_x-mid_x1))

                num += 1
                x += abs(mid_x-mid_x1)*1.0
                break
    print "average disp1: ", x/(num*1.0)
    print num
    # print np.mean(disp), np.min(disp), np.max(disp), np.std(disp, ddof=1)
    return disp

def main():
    ap_file = r'./Stereo/r_0_out.log'
    ap_res = get_ap_log(ap_file)
    ap_file1 = r'./Stereo/r_1_out.log'
    ap_res1 = get_ap_log1(ap_file1)

    #using key points

    disp1 = get_disp(ap_res, ap_res1)#gt
    disp2 = draw(ap_res)#pred
    print len(disp1), len(disp2)
    sleep_t = 0.001
    id = []
    disp = []
    total = 0.0
    num = 0
    for i in xrange(197):
        fig1 = plt.figure(1)
        plt.pause(sleep_t)
        plt.clf()
        # print i, abs(disp1[i]-disp2[i])
        for j in xrange(198):
            # print disp2[j][0]
            if disp1[i][0] == disp2[j][0]:
                # print disp1[i][0], disp2[j][0]
                total += abs(disp1[i][1] - disp2[j][1])
                id.append(num)
                num += 1
                disp.append(disp1[i][1] - disp2[j][1])
                # plt.axis([0, 200, -6, 6])
                plt.plot(id[0:], disp[0:], c='blue')
        # total += abs(disp1[i]-disp2[i])
        # id.append(i)
        # disp.append(disp1[i]-disp2[i])
        # plt.axis([0, 286, -20, 30])
        # plt.plot(id[0:], disp[0:], c='blue')
    print total/(num*1.0)
    print num
    plt.pause(10)
    plt.show()


    # manually

    # disp_img = np.array(Image.open('./Stereo/test_1215_disp_resize/000589.png'))/(16.0*16.0)
    # disp_img1 = np.array(Image.open('./Stereo/test_1215_disp_resize/000659.png')) / (16.0*16.0)
    # disp_img2 = np.array(Image.open('./Stereo/test_1215_disp_resize/000720.png')) / (16.0 * 16.0)
    #
    # # disp_img = np.array(Image.open('./Stereo/disp/000589.png')) / (16.0 * 16.0)
    # # disp_img1 = np.array(Image.open('./Stereo/disp/000659.png')) / (16.0 * 16.0)
    # # disp_img2 = np.array(Image.open('./Stereo/disp/000720.png')) / (16.0 * 16.0)
    # print disp_img[565][794], disp_img1[566][1020], disp_img2[566][1231]
    # # print disp_img1[566][1031]
    # # print disp_img2[566][1359]


if __name__ == '__main__':
    main()
